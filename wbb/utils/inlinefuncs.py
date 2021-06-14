"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import json
import os
import sys
from random import randint
from sys import version as pyver
from time import ctime, time

from motor import version as mongover
from pykeyboard import InlineKeyboard
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.raw.functions import Ping
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent)
from search_engine_parser import GoogleSearch

from wbb import (BOT_USERNAME, MESSAGE_DUMP_CHAT, SUDOERS, USERBOT_ID,
                 USERBOT_NAME, USERBOT_USERNAME, aiohttpsession, app, app2,
                 arq)
from wbb.core.types import InlineQueryResultCachedDocument
from wbb.modules.info import get_chat_info, get_user_info
from wbb.modules.music import download_youtube_audio
from wbb.utils.fetch import fetch
from wbb.utils.functions import test_speedtest
from wbb.utils.pastebin import paste

keywords_list = [
    "alive",
    "ping",
    "tr",
    "ud",
    "google",
    "bitly",
    "wall",
    "yt",
    "torrent",
    "lyrics",
    "wiki",
    "speedtest",
    "music",
    "gh_repo",
    "gh_user",
    "search",
    "ytmusic",
    "info",
    "chat_info",
    "tmdb",
    "pypi",
    "image",
]


async def inline_help_func(__HELP__):
    buttons = InlineKeyboard(row_width=4)
    buttons.add(
        *[
            (InlineKeyboardButton(text=i, switch_inline_query_current_chat=i))
            for i in keywords_list
        ]
    )
    answerss = [
        InlineQueryResultArticle(
            title="Inline Commands",
            description="Help Related To Inline Usage.",
            input_message_content=InputTextMessageContent(
                "Click A Button To Get Started."
            ),
            thumb_url="https://hamker.me/cy00x5x.png",
            reply_markup=buttons,
        ),
        InlineQueryResultArticle(
            title="Github Repo",
            description="Get Github Respository Of Bot.",
            input_message_content=InputTextMessageContent(
                "https://github.com/thehamkercat/WilliamButcherBot"
            ),
            thumb_url="https://hamker.me/gjc9fo3.png",
        ),
    ]
    answerss = await alive_function(answerss)
    return answerss


async def alive_function(answers):
    buttons = InlineKeyboard(row_width=2)
    bot_state = "Dead" if not await app.get_me() else "Alive"
    ubot_state = "Dead" if not await app2.get_me() else "Alive"
    buttons.add(
        InlineKeyboardButton("Stats", callback_data="stats_callback"),
        InlineKeyboardButton(
            "Go Inline!", switch_inline_query_current_chat=""
        ),
    )

    msg = f"""
**[William✨](https://github.com/thehamkercat/WilliamButcherBot):**
**MainBot:** `{bot_state}`
**UserBot:** `{ubot_state}`
**Python:** `{pyver.split()[0]}`
**Pyrogram:** `{pyrover}`
**MongoDB:** `{mongover}`
**Platform:** `{sys.platform}`
**Profiles:** [BOT](t.me/{BOT_USERNAME}) | [UBOT](t.me/{USERBOT_USERNAME})
"""
    answers.append(
        InlineQueryResultArticle(
            title="Alive",
            description="Check Bot's Stats",
            thumb_url="https://static2.aniimg.com/upload/20170515/414/c/d/7/cd7EEF.jpg",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=buttons,
        )
    )
    return answers


async def translate_func(answers, lang, tex):
    result = await arq.translate(tex, lang)
    if not result.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=result.result,
                input_message_content=InputTextMessageContent(result.result),
            )
        )
        return answers
    result = result.result
    msg = f"""
__**Translated from {result.src} to {result.dest}**__

**INPUT:**
{tex}

**OUTPUT:**
{result.translatedText}"""
    answers.extend(
        [
            InlineQueryResultArticle(
                title=f"Translated from {result.src} to {result.dest}.",
                description=result.translatedText,
                input_message_content=InputTextMessageContent(msg),
            ),
            InlineQueryResultArticle(
                title=result.translatedText,
                input_message_content=InputTextMessageContent(
                    result.translatedText
                ),
            ),
        ]
    )
    return answers


async def urban_func(answers, text):
    results = await arq.urbandict(text)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[0:48]
    for i in results:
        msg = f"""
**Query:** {text}

**Definition:** __{i.definition}__

**Example:** __{i.example}__"""

        answers.append(
            InlineQueryResultArticle(
                title=i.word,
                description=i.definition,
                input_message_content=InputTextMessageContent(msg),
            )
        )
    return answers


async def google_search_func(answers, text):
    gresults = await GoogleSearch().async_search(text)
    limit = 0
    for i in gresults:
        if limit > 48:
            break
        limit += 1

        try:
            msg = f"""
[{i['titles']}]({i['links']})
{i['descriptions']}"""

            answers.append(
                InlineQueryResultArticle(
                    title=i["titles"],
                    description=i["descriptions"],
                    input_message_content=InputTextMessageContent(
                        msg, disable_web_page_preview=True
                    ),
                )
            )
        except KeyError:
            pass
    return answers


async def wall_func(answers, text):
    results = await arq.wall(text)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[0:48]
    for i in results:
        answers.append(
            InlineQueryResultPhoto(
                photo_url=i.url_image,
                thumb_url=i.url_thumb,
                caption=f"[Source]({i.url_image})",
            )
        )
    return answers


# Used my api key here, don't fuck it
async def shortify(url):
    if "." not in url:
        return
    header = {
        "Authorization": "Bearer ad39983fa42d0b19e4534f33671629a4940298dc",
        "Content-Type": "application/json",
    }
    payload = {"long_url": f"{url}"}
    payload = json.dumps(payload)
    async with aiohttpsession.post(
        "https://api-ssl.bitly.com/v4/shorten",
        headers=header,
        data=payload,
    ) as resp:
        data = await resp.json()
    msg = data["link"]
    a = []
    b = InlineQueryResultArticle(
        title="Link Shortened!",
        description=data["link"],
        input_message_content=InputTextMessageContent(
            msg, disable_web_page_preview=True
        ),
    )
    a.append(b)
    return a


async def torrent_func(answers, text):
    results = await arq.torrent(text)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[0:48]
    for i in results:
        title = i.name
        size = i.size
        seeds = i.seeds
        leechs = i.leechs
        upload_date = i.uploaded
        magnet = i.magnet
        caption = f"""
**Title:** __{title}__
**Size:** __{size}__
**Seeds:** __{seeds}__
**Leechs:** __{leechs}__
**Uploaded:** __{upload_date}__
**Magnet:** `{magnet}`"""

        description = f"{size} | {upload_date} | Seeds: {seeds}"
        answers.append(
            InlineQueryResultArticle(
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    caption, disable_web_page_preview=True
                ),
            )
        )
        pass
    return answers


async def youtube_func(answers, text):
    results = await arq.youtube(text)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[0:48]
    for i in results:
        buttons = InlineKeyboard(row_width=1)
        video_url = f"https://youtube.com{i.url_suffix}"
        buttons.add(InlineKeyboardButton("Watch", url=video_url))
        caption = f"""
**Title:** {i.title}
**Views:** {i.views}
**Channel:** {i.channel}
**Duration:** {i.duration}
**Uploaded:** {i.publish_time}
**Description:** {i.long_desc}"""
        description = (
            f"{i.views} | {i.channel} | {i.duration} | {i.publish_time}"
        )
        answers.append(
            InlineQueryResultArticle(
                title=i.title,
                thumb_url=i.thumbnails[0],
                description=description,
                input_message_content=InputTextMessageContent(
                    caption, disable_web_page_preview=True
                ),
                reply_markup=buttons,
            )
        )
    return answers


async def lyrics_func(answers, text):
    song = await arq.lyrics(text)
    if not song.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=song.result,
                input_message_content=InputTextMessageContent(song.result),
            )
        )
        return answers
    lyrics = song.result
    song = lyrics.splitlines()
    song_name = song[0]
    artist = song[1]
    if len(lyrics) > 4095:
        lyrics = await paste(lyrics)
        lyrics = f"**LYRICS_TOO_LONG:** [URL]({lyrics})"

    msg = f"__{lyrics}__"

    answers.append(
        InlineQueryResultArticle(
            title=song_name,
            description=artist,
            input_message_content=InputTextMessageContent(msg),
        )
    )
    return answers


async def github_user_func(answers, text):
    URL = f"https://api.github.com/users/{text}"
    result = await fetch(URL)
    buttons = InlineKeyboard(row_width=1)
    buttons.add(
        InlineKeyboardButton(
            text="Open On Github", url=f"https://github.com/{text}"
        )
    )
    caption = f"""
**Info Of {result['name']}**
**Username:** `{text}`
**Bio:** `{result['bio']}`
**Profile Link:** [Here]({result['html_url']})
**Company:** `{result['company']}`
**Created On:** `{result['created_at']}`
**Repositories:** `{result['public_repos']}`
**Blog:** `{result['blog']}`
**Location:** `{result['location']}`
**Followers:** `{result['followers']}`
**Following:** `{result['following']}`"""
    answers.append(
        InlineQueryResultPhoto(
            photo_url=result["avatar_url"],
            caption=caption,
            reply_markup=buttons,
        )
    )
    return answers


async def github_repo_func(answers, text):
    text = text.replace("https://github.com/", "")
    text = text.replace("http://github.com/", "")
    if text[-1] == "/":
        text = text[0:-1]
    URL = f"https://api.github.com/repos/{text}"
    URL2 = f"https://api.github.com/repos/{text}/contributors"
    results = await asyncio.gather(fetch(URL), fetch(URL2))
    r = results[0]
    r1 = results[1]
    commits = 0
    for developer in r1:
        commits += developer["contributions"]
    buttons = InlineKeyboard(row_width=1)
    buttons.add(
        InlineKeyboardButton(
            "Open On Github", url=f"https://github.com/{text}"
        )
    )
    caption = f"""
**Info Of {r['full_name']}**
**Stars:** `{r['stargazers_count']}`
**Watchers:** `{r['watchers_count']}`
**Forks:** `{r['forks_count']}`
**Commits:** `{commits}`
**Is Fork:** `{r['fork']}`
**Language:** `{r['language']}`
**Contributors:** `{len(r1)}`
**License:** `{r['license']['name'] if r['license'] else None}`
**Repo Owner:** [{r['owner']['login']}]({r['owner']['html_url']})
**Created On:** `{r['created_at']}`
**Homepage:** {r['homepage']}
**Description:** __{r['description']}__"""
    answers.append(
        InlineQueryResultArticle(
            title="Found Repo",
            description=text,
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(
                caption, disable_web_page_preview=True
            ),
        )
    )
    return answers


async def tg_search_func(answers, text, user_id):
    if user_id not in SUDOERS:
        msg = "**ERROR**\n__THIS FEATURE IS ONLY FOR SUDO USERS__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="THIS FEATURE IS ONLY FOR SUDO USERS",
                input_message_content=InputTextMessageContent(msg),
            )
        )
        return answers
    if str(text)[-1] != ":":
        msg = "**ERROR**\n__Put A ':' After The Text To Search__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="Put A ':' After The Text To Search",
                input_message_content=InputTextMessageContent(msg),
            )
        )

        return answers
    text = text[0:-1]
    async for message in app2.search_global(text, limit=49):
        buttons = InlineKeyboard(row_width=2)
        buttons.add(
            InlineKeyboardButton(
                text="Origin",
                url=message.link if message.link else "https://t.me/telegram",
            ),
            InlineKeyboardButton(
                text="Search again", switch_inline_query_current_chat="search"
            ),
        )
        name = (
            message.from_user.first_name
            if message.from_user.first_name
            else "NO NAME"
        )
        caption = f"""
**Query:** {text}
**Name:** {str(name)} [`{message.from_user.id}`]
**Chat:** {str(message.chat.title)} [`{message.chat.id}`]
**Date:** {ctime(message.date)}
**Text:** >>

{message.text.markdown if message.text else message.caption if message.caption else '[NO_TEXT]'}
"""
        result = InlineQueryResultArticle(
            title=name,
            description=message.text if message.text else "[NO_TEXT]",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(
                caption, disable_web_page_preview=True
            ),
        )
        answers.append(result)
    return answers


async def music_inline_func(answers, query):
    chat_id = -1001445180719
    group_invite = "https://t.me/joinchat/vSDE2DuGK4Y4Nzll"
    try:
        messages = [
            m
            async for m in app2.search_messages(
                chat_id, query, filter="audio", limit=199
            )
        ]
    except Exception as e:
        print(e)
        msg = f"You Need To Join Here With Your Bot And Userbot To Get Cached Music.\n{group_invite}"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="Click Here To Know More.",
                input_message_content=InputTextMessageContent(
                    msg, disable_web_page_preview=True
                ),
            )
        )
        return answers
    messages_ids_and_duration = []
    for f_ in messages:
        messages_ids_and_duration.append(
            {
                "message_id": f_.message_id,
                "duration": f_.audio.duration if f_.audio.duration else 0,
            }
        )
    messages = list(
        {v["duration"]: v for v in messages_ids_and_duration}.values()
    )
    messages_ids = []
    for ff_ in messages:
        messages_ids.append(ff_["message_id"])
    messages = await app.get_messages(chat_id, messages_ids[0:48])
    for message_ in messages:
        answers.append(
            InlineQueryResultCachedDocument(
                file_id=message_.audio.file_id, title=message_.audio.title
            )
        )
    return answers


async def wiki_func(answers, text):
    data = await arq.wiki(text)
    if not data.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=data.result,
                input_message_content=InputTextMessageContent(data.result),
            )
        )
        return answers
    data = data.result
    msg = f"""
**QUERY:**
{data.title}

**ANSWER:**
__{data.answer}__"""
    answers.append(
        InlineQueryResultArticle(
            title=data.title,
            description=data.answer,
            input_message_content=InputTextMessageContent(msg),
        )
    )
    return answers


async def speedtest_init(query):
    answers = []
    user_id = query.from_user.id
    if user_id not in SUDOERS:
        msg = "**ERROR**\n__THIS FEATURE IS ONLY FOR SUDO USERS__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="THIS FEATURE IS ONLY FOR SUDO USERS",
                input_message_content=InputTextMessageContent(msg),
            )
        )
        return answers
    msg = "**Click The Button Below To Perform A Speedtest**"
    button = InlineKeyboard(row_width=1)
    button.add(
        InlineKeyboardButton(text="Test", callback_data="test_speedtest")
    )
    answers.append(
        InlineQueryResultArticle(
            title="Click Here",
            input_message_content=InputTextMessageContent(msg),
            reply_markup=button,
        )
    )
    return answers


""" callback query for the function above """


@app.on_callback_query(filters.regex("test_speedtest"))
async def test_speedtest_cq(_, cq):
    if cq.from_user.id not in SUDOERS:
        return await cq.answer("This Isn't For You!")
    inline_message_id = cq.inline_message_id
    await app.edit_inline_text(inline_message_id, "**Testing**")
    loop = asyncio.get_running_loop()
    download, upload, info = await loop.run_in_executor(None, test_speedtest)
    msg = f"""
**Download:** `{download}`
**Upload:** `{upload}`
**Latency:** `{info['latency']} ms`
**Country:** `{info['country']} [{info['cc']}]`
**Latitude:** `{info['lat']}`
**Longitude:** `{info['lon']}`
"""
    await app.edit_inline_text(inline_message_id, msg)


async def pmpermit_func(answers, user_id, victim):
    if user_id != USERBOT_ID:
        return
    caption = f"Hi, I'm {USERBOT_NAME}, What are you here for?, You'll be blocked if you send more than 5 messages."
    buttons = InlineKeyboard(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            text="To Scam You", callback_data="pmpermit to_scam_you a"
        ),
        InlineKeyboardButton(
            text="For promotion", callback_data="pmpermit to_scam_you a"
        ),
        InlineKeyboardButton(
            text="Approve me", callback_data="pmpermit approve_me a"
        ),
        InlineKeyboardButton(
            text="Approve", callback_data=f"pmpermit approve {victim}"
        ),
    )
    answers.append(
        InlineQueryResultArticle(
            title="do_not_click_here",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(caption),
        )
    )
    return answers


async def ping_func(answers):
    t1 = time()
    ping = Ping(ping_id=randint(696969, 6969696))
    await app.send(ping)
    t2 = time()
    ping = f"{str(round((t2 - t1), 6) * 100)} ms"
    answers.append(
        InlineQueryResultArticle(
            title=ping,
            input_message_content=InputTextMessageContent(f"__**{ping}**__"),
        )
    )
    return answers


async def yt_music_func(answers, url):
    if "http" not in url:
        url = (await arq.youtube(url)).result[0]
        url = f"https://youtube.com{url.url_suffix}"
    loop = asyncio.get_running_loop()
    music = await loop.run_in_executor(None, download_youtube_audio, url)
    if not music:
        msg = "**ERROR**\n__MUSIC TOO LONG__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="MUSIC TOO LONG",
                input_message_content=InputTextMessageContent(msg),
            )
        )
        return answers
    (
        title,
        performer,
        duration,
        audio,
        thumbnail,
    ) = music
    m = await app.send_audio(
        MESSAGE_DUMP_CHAT,
        audio,
        title=title,
        duration=duration,
        performer=performer,
        thumb=thumbnail,
    )
    os.remove(audio)
    os.remove(thumbnail)
    answers.append(
        InlineQueryResultCachedDocument(title=title, file_id=m.audio.file_id)
    )
    return answers


async def user_info_inline_func(answers, user):
    try:
        caption, _ = await get_user_info(user)
    except Exception:
        answers.append(
            InlineQueryResultArticle(
                title="USER NOT FOUND",
                input_message_content=InputTextMessageContent(
                    "USER NOT FOUND"
                ),
            )
        )
        return answers
    answers.append(
        InlineQueryResultArticle(
            title="Found User.",
            input_message_content=InputTextMessageContent(
                caption, disable_web_page_preview=True
            ),
        )
    )
    return answers


async def chat_info_inline_func(answers, chat):
    caption, photo_id = await get_chat_info(chat)
    answers.append(
        InlineQueryResultArticle(
            title="Found Chat.",
            input_message_content=InputTextMessageContent(
                caption, disable_web_page_preview=True
            ),
        )
    )
    return answers


async def tmdb_func(answers, query):
    response = await arq.tmdb(query)
    if not response.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=response.result,
                input_message_content=InputTextMessageContent(response.result),
            )
        )
        return answers
    results = response.result[0:48]
    for result in results:
        if not result.poster and not result.backdrop:
            continue
        if not result.genre:
            genre = None
        else:
            genre = " | ".join(result.genre)
        description = result.overview[0:900] if result.overview else "None"
        caption = f"""
**{result.title}**
**Type:** {result.type}
**Rating:** {result.rating}
**Genre:** {genre}
**Release Date:** {result.releaseDate}
**Description:** __{description}__
"""
        buttons = InlineKeyboard(row_width=1)
        buttons.add(
            InlineKeyboardButton(
                "Search Again", switch_inline_query_current_chat="tmdb"
            )
        )
        answers.append(
            InlineQueryResultPhoto(
                photo_url=result.backdrop
                if result.backdrop
                else result.poster,
                caption=caption,
                title=result.title,
                description=f"{genre} • {result.releaseDate} • {result.rating} • {description}",
                reply_markup=buttons,
            )
        )
    return answers


async def pypiSearchFunc(answers: list, query: str) -> list:
    result = await arq.pypi(query)
    if not result.ok:
        answers.append(
            InlineQueryResultArticle(
                title="No Such Package",
                description=result.result,
                input_message_content=InputTextMessageContent(result.result),
            )
        )
        return answers
    result = result.result
    pURLS = [
        f"**{key}**: {value}" for key, value in result.projectURLS.items()
    ]
    pURLS = ("\n" + "\n".join(pURLS)) if pURLS else None
    caption = f"""
**Name:** {result.name}
**Version:** {result.version}
**License:** {result.license}
**Description:** {result.description}
**Size:** {result.size}
**Last Update:** {result.uploadTime}
**Author:** {result.author}
**Author's Email:** {result.authorEmail}
**Requirements:** {(f'`{" | ".join(result.requirements)}`') if result.requirements else None}
**Minimum Python Version:** {result.minPyVersion}
**Homepage:** {result.homepage}
**Bug Tracker:** {result.bugTrackURL}
**Docs Url:** {result.docsURL}
**Pypi Url:** {result.pypiURL}
**Releases:** {result.releaseURL}
**Project Urls:** ->{pURLS}
"""
    button = InlineKeyboard(row_width=2)
    button.add(
        InlineKeyboardButton(text="Open Page", url=result.pypiURL),
        InlineKeyboardButton(
            text="Search Again", switch_inline_query_current_chat="pypi"
        ),
    )
    answers.append(
        InlineQueryResultArticle(
            title=f"{result.name}  |  {result.version}",
            description=result.description,
            input_message_content=InputTextMessageContent(
                caption, disable_web_page_preview=True
            ),
            reply_markup=button,
        )
    )
    return answers


async def image_func(answers, query):
    results = await arq.image(query)
    if not results.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=results.result,
                input_message_content=InputTextMessageContent(results.result),
            )
        )
        return answers
    results = results.result[0:48]
    buttons = InlineKeyboard(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            text="Search again", switch_inline_query_current_chat="image"
        ),
    )
    for i in results:
        answers.append(
            InlineQueryResultPhoto(
                title=i.title,
                photo_url=i.url,
                thumb_url=i.url,
                reply_markup=buttons,
            )
        )
    return answers
