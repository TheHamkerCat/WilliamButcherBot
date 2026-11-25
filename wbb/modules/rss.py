from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio import get_event_loop, sleep
from io import BytesIO
from urllib.parse import urljoin

from aiohttp import (
    ClientError,
    ClientSession,
    ClientTimeout,
    DummyCookieJar,
    TCPConnector,
)
from feedparser import parse
from pyrogram import filters
from pyrogram.errors import (
    ChannelInvalid,
    ChannelPrivate,
    InputUserDeactivated,
    UserIsBlocked,
)
from pyrogram.types import Message

from wbb import RSS_DELAY, app, log
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.utils.dbfunctions import (
    add_rss_feed,
    get_rss_feeds,
    is_rss_active,
    remove_rss_feed,
    update_rss_feed,
)
from wbb.utils.functions import SafeResolver, get_urls_from_text, is_safe_url
from wbb.utils.rss import Feed

__MODULE__ = "RSS"
__HELP__ = f"""
/add_feed [URL] - Add a feed to chat
/rm_feed - Remove feed from chat

**Note:**
    - This will check for updates every {RSS_DELAY // 60} minutes.
    - You can only add one feed per chat.
    - Currently RSS and ATOM feeds are supported.
"""


MAX_REDIRECTS = 3
MAX_FEED_BYTES = 2_000_000
FEED_TIMEOUT = ClientTimeout(total=10)


class TransientFeedError(Exception):
    """A feed fetch that can succeed on the next poll."""


def parse_feed(body: bytes, url: str):
    # A stream keeps feedparser from opening the body as a local filename.
    return parse(
        BytesIO(body),
        response_headers={"content-location": url},
    )


async def fetch_feed(url: str):
    resolver = SafeResolver()
    connector = TCPConnector(resolver=resolver, use_dns_cache=False)
    try:
        async with ClientSession(
            connector=connector,
            timeout=FEED_TIMEOUT,
            cookie_jar=DummyCookieJar(),
            trust_env=False,
        ) as session:
            for _ in range(MAX_REDIRECTS + 1):
                if not is_safe_url(url):
                    raise ValueError("URL is not allowed")

                try:
                    async with session.get(
                        url,
                        allow_redirects=False,
                    ) as response:
                        if response.status in (301, 302, 303, 307, 308):
                            location = response.headers.get("Location")
                            if not location:
                                raise ValueError("Invalid redirect")
                            url = urljoin(url, location)
                            continue

                        if response.status != 200:
                            raise TransientFeedError(
                                f"Feed returned HTTP {response.status}"
                            )

                        chunks = []
                        size = 0
                        while True:
                            chunk = await response.content.read(64 * 1024)
                            if not chunk:
                                break
                            size += len(chunk)
                            if size > MAX_FEED_BYTES:
                                raise ValueError("Feed is too large")
                            chunks.append(chunk)
                        return b"".join(chunks), url
                except ValueError:
                    raise
                except (ClientError, AsyncioTimeoutError) as exc:
                    raise TransientFeedError(str(exc)) from exc
    finally:
        await connector.close()
        await resolver.close()

    raise ValueError("Too many redirects")


async def rss_worker():
    log.info("RSS Worker started")
    while not await sleep(RSS_DELAY):
        feeds = await get_rss_feeds()
        if not feeds:
            continue

        loop = get_event_loop()

        for _feed in feeds:
            chat = _feed["chat_id"]
            try:
                url = _feed["url"]
                last_title = _feed.get("last_title")

                body, final_url = await fetch_feed(url)
                parsed = await loop.run_in_executor(
                    None, parse_feed, body, final_url
                )
                feed = Feed(parsed)

                if feed.title == last_title:
                    continue

                await app.send_message(
                    chat, feed.parsed(), disable_web_page_preview=True
                )
                await update_rss_feed(chat, feed.title)
            except TransientFeedError as e:
                log.info(f"RSS in {chat}: {e}")
            except ValueError as e:
                await remove_rss_feed(chat)
                log.info(f"Removed RSS Feed from {chat} ({e})")
            except (
                ChannelInvalid,
                ChannelPrivate,
                InputUserDeactivated,
                UserIsBlocked,
                AttributeError,
            ):
                await remove_rss_feed(chat)
                log.info(f"Removed RSS Feed from {chat} (Invalid Chat)")
            except Exception as e:
                log.info(f"RSS in {chat}: {str(e)}")


loop = get_event_loop()
loop.create_task(rss_worker())


@app.on_message(filters.command("add_feed") & ~filters.private)
@adminsOnly("can_change_info")
@capture_err
async def add_feed_func(_, m: Message):
    if len(m.command) != 2:
        return await m.reply("Read 'RSS' section in help menu.")
    url = m.text.split(None, 1)[1].strip()

    if not url:
        return await m.reply("[ERROR]: Invalid Argument")

    urls = get_urls_from_text(url)
    if not urls:
        return await m.reply("[ERROR]: Invalid URL")

    url = urls[0]
    ns = "[ERROR]: This feed isn't supported."
    try:
        body, final_url = await fetch_feed(url)
    except (TransientFeedError, ValueError) as e:
        return await m.reply(f"[ERROR]: {e}")
    except Exception:
        return await m.reply(ns)
    try:
        loop = get_event_loop()
        parsed = await loop.run_in_executor(
            None, parse_feed, body, final_url
        )
        feed = Feed(parsed)
    except Exception:
        return await m.reply(ns)
    if not feed:
        return await m.reply(ns)

    chat_id = m.chat.id
    if await is_rss_active(chat_id):
        return await m.reply("[ERROR]: You already have an RSS feed enabled.")
    try:
        await m.reply(feed.parsed(), disable_web_page_preview=True)
    except Exception:
        return await m.reply(ns)
    await add_rss_feed(chat_id, final_url, feed.title)


@app.on_message(filters.command("rm_feed") & ~filters.private)
@adminsOnly("can_change_info")
async def rm_feed_func(_, m: Message):
    if await is_rss_active(m.chat.id):
        await remove_rss_feed(m.chat.id)
        await m.reply("Removed RSS Feed")
    else:
        await m.reply("There are no active RSS Feeds in this chat.")


@app.on_message(filters.command("rm_feed") & filters.private)
@capture_err
async def rm_feed_private(_, m: Message):
    # Old versions allowed feeds in private chats; let their owners remove them.
    if await is_rss_active(m.chat.id):
        await remove_rss_feed(m.chat.id)
        await m.reply("Removed RSS Feed")
    else:
        await m.reply("There are no active RSS Feeds in this chat.")
