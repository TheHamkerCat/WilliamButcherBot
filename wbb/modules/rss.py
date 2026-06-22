from asyncio import get_event_loop, sleep

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
from wbb.utils.dbfunctions import (
    add_rss_feed,
    get_rss_feeds,
    is_rss_active,
    remove_rss_feed,
    update_rss_feed,
)
from wbb.utils.functions import (
    get_http_status_code,
    get_urls_from_text,
    is_safe_url,
)
from wbb.utils.rss import Feed

__MODULE__ = "RSS"
__HELP__ = f"""
/add_feed [الرابط] - إضافة خلاصة إلى المحادثة
/rm_feed - إزالة خلاصة من المحادثة

**ملاحظة:**
    - سيتحقق من التحديثات كل {RSS_DELAY // 60} دقيقة.
    - يمكنك إضافة خلاصة واحدة فقط لكل محادثة.
    - يدعم حالياً خلاصات RSS و ATOM.
"""


def get_parsed_feed_url(parsed, fallback: str) -> str:
    href = parsed.get("href")
    if isinstance(href, str) and href:
        return href
    return fallback


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
                if not is_safe_url(url):
                    await remove_rss_feed(chat)
                    log.info(f"Removed RSS Feed from {chat} (Unsafe URL)")
                    continue

                last_title = _feed.get("last_title")

                parsed = await loop.run_in_executor(None, parse, url)
                final_url = get_parsed_feed_url(parsed, url)
                if not is_safe_url(final_url):
                    await remove_rss_feed(chat)
                    log.info(f"Removed RSS Feed from {chat} (Unsafe redirect)")
                    continue

                feed = Feed(parsed)

                if feed.title == last_title:
                    continue

                await app.send_message(
                    chat, feed.parsed(), disable_web_page_preview=True
                )
                await update_rss_feed(chat, feed.title)
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


@app.on_message(filters.command("add_feed"))
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
    if not is_safe_url(url):
        return await m.reply("[ERROR]: URL is not allowed (SSRF protection).")

    status = await get_http_status_code(url)
    if status != 200:
        return await m.reply("[ERROR]: Invalid Url")

    ns = "[ERROR]: This feed isn't supported."
    try:
        loop = get_event_loop()
        parsed = await loop.run_in_executor(None, parse, url)
        final_url = get_parsed_feed_url(parsed, url)
        if not is_safe_url(final_url):
            return await m.reply("[ERROR]: URL is not allowed (SSRF protection).")

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


@app.on_message(filters.command("rm_feed"))
async def rm_feed_func(_, m: Message):
    if await is_rss_active(m.chat.id):
        await remove_rss_feed(m.chat.id)
        await m.reply("Removed RSS Feed")
    else:
        await m.reply("There are no active RSS Feeds in this chat.")
