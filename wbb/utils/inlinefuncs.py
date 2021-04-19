import aiohttp
import json
import sys
import asyncio
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineQueryResultPhoto
)
from googletrans import Translator
from search_engine_parser import GoogleSearch
from pykeyboard import InlineKeyboard
from sys import version as pyver
from motor import version as mongover
from pyrogram import __version__ as pyrover
from time import time, ctime
from wbb.modules.userbot import eval_executor_func
from wbb.utils.fetch import fetch
from wbb.utils.formatter import convert_seconds_to_minutes as time_convert
from wbb.utils.pastebin import paste
from wbb import (
    arq, app, app2, USERBOT_USERNAME,
    BOT_USERNAME, LOG_GROUP_ID, USERBOT_ID
)
from wbb.core.types.InlineQueryResult import InlineQueryResultAudio


async def deezaudio_func(answers):
    msg = "a"
    answers.append(
        InlineQueryResultAudio(
            audio_url="https://masstamilan2019download.com/tamil/2019%20Tamil%20Mp3/Oh%20My%20Kadavule/Kadhaippoma-Masstamilan.In.mp3",
            title="a",
            description="desc",
            input_message_content=InputTextMessageContent(msg)
        )
    )
    return answers





async def inline_help_func(__HELP__):
    buttons = InlineKeyboard(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            'Get More Help.',
            url=f"t.me/{BOT_USERNAME}?start=start"
        ),
        InlineKeyboardButton(
            "Go Inline!",
            switch_inline_query_current_chat=""
        )
    )
    answerss = [
        InlineQueryResultArticle(
            title="Inline Commands",
            description="Help Related To Inline Usage.",
            input_message_content=InputTextMessageContent(__HELP__),
            thumb_url="https://hamker.me/cy00x5x.png",
            reply_markup=buttons
        )
    ]
    answerss = await alive_function(answerss)
    return answerss


async def alive_function(answers):
    buttons = InlineKeyboard(row_width=2)
    bot_state = 'Dead' if not await app.get_me() else 'Alive'
    ubot_state = 'Dead' if not await app2.get_me() else 'Alive'
    buttons.add(
        InlineKeyboardButton(
            'Stats',
            callback_data='stats_callback'
        ),
        InlineKeyboardButton(
            "Go Inline!",
            switch_inline_query_current_chat=""
        )
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
            title='Alive',
            description="Check Bot's Stats",
            thumb_url="https://static2.aniimg.com/upload/20170515/414/c/d/7/cd7EEF.jpg",
            input_message_content=InputTextMessageContent(
                msg,
                disable_web_page_preview=True
            ),
            reply_markup=buttons,
        )
    )
    return answers


async def translate_func(answers, lang, tex):
    i = Translator().translate(tex, dest=lang)
    msg = f"""
__**Translated to {lang}**__

**INPUT:**
{tex}

**OUTPUT:**
{i.text}"""
    answers.append(
        InlineQueryResultArticle(
            title=f'Translated to {lang}',
            description=i.text,
            input_message_content=InputTextMessageContent(msg)
        )
    )
    return answers


async def urban_func(answers, text):
    results = await arq.urbandict(text)
    limit = 0
    for i in results:
        if limit > 48:
            break
        limit += 1
        msg = f"""
**Query:** {text}

**Definition:** __{results[i].definition}__

**Example:** __{results[i].example}__"""

        answers.append(
            InlineQueryResultArticle(
                title=results[i].word,
                description=results[i].definition,
                input_message_content=InputTextMessageContent(msg)
            ))
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
                    title=i['titles'],
                    description=i['descriptions'],
                    input_message_content=InputTextMessageContent(
                        msg,
                        disable_web_page_preview=True
                    )
                ))
        except KeyError:
            pass
    return answers


async def wall_func(answers, text):
    results = await arq.wall(text)
    limit = 0
    for i in results:
        if limit > 48:
            break
        limit += 1
        try:
            answers.append(
                InlineQueryResultPhoto(
                    photo_url=results[i].url_image,
                    thumb_url=results[i].url_thumb,
                    caption=f"[Source]({results[i].url_image})"
                ))
        except KeyError:
            pass
    return answers


async def saavn_func(answers, text):
    buttons_list = []
    results = await arq.saavn(text)
    for i in results:
        buttons = InlineKeyboard(row_width=1)
        buttons.add(
            InlineKeyboardButton(
                'Download | Play',
                url=results[i].media_url
            )
        )
        buttons_list.append(buttons)
        duration = await time_convert(results[i].duration)
        caption = f"""
**Title:** {results[i].song}
**Album:** {results[i].album}
**Duration:** {duration}
**Release:** {results[i].year}
**Singers:** {results[i].singers}"""
        description = f"{results[i].album} | {duration} " \
            + f"| {results[i].singers} ({results[i].year})"
        try:
            answers.append(
                InlineQueryResultArticle(
                    title=results[i].song,
                    input_message_content=InputTextMessageContent(
                        caption,
                        disable_web_page_preview=True
                    ),
                    description=description,
                    thumb_url=results[i].image,
                    reply_markup=buttons_list[i]
                ))
        except (KeyError, ValueError):
            pass
    return answers


async def deezer_func(answers, text):
    buttons_list = []
    results = await arq.deezer(text, 5)
    for i in results:
        buttons = InlineKeyboard(row_width=1)
        buttons.add(
            InlineKeyboardButton(
                'Download | Play',
                url=results[i].url
            )
        )
        buttons_list.append(buttons)
        duration = await time_convert(results[i].duration)
        caption = f"""
**Title:** {results[i].title}
**Artist:** {results[i].artist}
**Duration:** {duration}
**Source:** [Deezer]({results[i].source})"""
        description = f"{results[i].artist} | {duration}"
        try:
            answers.append(
                InlineQueryResultArticle(
                    title=results[i].title,
                    thumb_url=results[i].thumbnail,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        caption,
                        disable_web_page_preview=True
                    ),
                    reply_markup=buttons_list[i]
                ))
        except (KeyError, ValueError):
            pass
    return answers


async def webss(url):
    start_time = time()
    if "." not in url:
        return
    screenshot = await fetch(f"https://patheticprogrammers.cf/ss?site={url}")
    end_time = time()
    try:
        m = await app.send_photo(LOG_GROUP_ID, photo=screenshot['url'])
    except TypeError:
        return
    await m.delete()
    a = []
    pic = InlineQueryResultPhoto(
        photo_url=screenshot['url'],
        caption=(f"`{url}`\n__Took {round(end_time - start_time)} Seconds.__")
    )
    a.append(pic)
    return a


# Used my api key here, don't fuck with it
async def shortify(url):
    if "." not in url:
        return
    header = {
        "Authorization": "Bearer ad39983fa42d0b19e4534f33671629a4940298dc",
        'Content-Type': 'application/json'
    }
    payload = {
        "long_url": f"{url}"
    }
    payload = json.dumps(payload)
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api-ssl.bitly.com/v4/shorten", headers=header, data=payload) as resp:
            data = await resp.json()
    msg = f"**Original Url:** {url}\n**Shortened Url:** {data['link']}"
    a = []
    b = InlineQueryResultArticle(
        title="Link Shortened!",
        description=data['link'],
        input_message_content=InputTextMessageContent(
            msg, disable_web_page_preview=True)
    )
    a.append(b)
    return a


async def torrent_func(answers, text):
    results = await arq.torrent(text)
    limit = 0
    for i in results:
        if limit > 48:
            break
        title = results[i].name
        size = results[i].size
        seeds = results[i].seeds
        leechs = results[i].leechs
        upload_date = results[i].uploaded + " Ago"
        magnet = results[i].magnet
        caption = f"""
**Title:** __{title}__
**Size:** __{size}__
**Seeds:** __{seeds}__
**Leechs:** __{leechs}__
**Uploaded:** __{upload_date}__
**Magnet:** __{magnet}__"""

        description = f"{size} | {upload_date} | Seeds: {seeds}"
        try:
            answers.append(
                InlineQueryResultArticle(
                    title=title,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        caption,
                        disable_web_page_preview=True
                    )
                )
            )
            limit += 1
        except (KeyError, ValueError):
            pass
    return answers


async def youtube_func(answers, text):
    results = await arq.youtube(text)
    limit = 0
    for i in results:
        if limit > 48:
            break
        limit += 1
        buttons = InlineKeyboard(row_width=1)
        video_url = f"https://youtube.com{results[i].url_suffix}"
        buttons.add(
            InlineKeyboardButton(
                'Watch',
                url=video_url
            )
        )
        caption = f"""
**Title:** {results[i].title}
**Views:** {results[i].views}
**Channel:** {results[i].channel}
**Duration:** {results[i].duration}
**Uploaded:** {results[i].publish_time}
**Description:** {results[i].long_desc}"""
        description = f"{results[i].views} | {results[i].channel} | " \
            + f"{results[i].duration} | {results[i].publish_time}"
        try:
            answers.append(
                InlineQueryResultArticle(
                    title=results[i].title,
                    thumb_url=results[i].thumbnails[0],
                    description=description,
                    input_message_content=InputTextMessageContent(
                        caption,
                        disable_web_page_preview=True
                    ),
                    reply_markup=buttons
                ))
        except (KeyError, ValueError):
            pass
    return answers


async def lyrics_func(answers, text):
    song = await arq.lyrics(text)
    lyrics = song.lyrics
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
            input_message_content=InputTextMessageContent(msg)
        ))
    return answers


async def eval_func(answers, text, user_id):
    if user_id != USERBOT_ID:
        msg = "**ERROR**\n__THIS FEATURE IS ONLY FOR SUDO USERS__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="THIS FEATURE IS ONLY FOR SUDO USERS",
                input_message_content=InputTextMessageContent(msg)
            ))
        return answers
    if str(text)[-1] != ":":
        msg = "**ERROR**\n__Put A ':' After The Code To Execute It__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="Put A ':' After The Code To Execute It",
                input_message_content=InputTextMessageContent(msg)
            ))

        return answers
    text = text[0:-1]
    start_time = time()
    result = await eval_executor_func(text)
    output = result[1]
    result = result[0]
    msg = f"{result}"
    end_time = time()
    answers.append(
        InlineQueryResultArticle(
            title=f"Took {round(end_time - start_time)} Seconds.",
            description=output,
            input_message_content=InputTextMessageContent(msg)
        ))
    return answers


async def github_user_func(answers, text):
    URL = f"https://api.github.com/users/{text}"
    result = await fetch(URL)
    buttons = InlineKeyboard(row_width=1)
    buttons.add(InlineKeyboardButton(
        text="Open On Github",
        url=f"https://github.com/{text}"
    ))
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
            photo_url=result['avatar_url'],
            caption=caption,
            reply_markup=buttons
        ))
    return answers


async def github_repo_func(answers, text):
    URL = f"https://api.github.com/repos/{text}"
    URL2 = f"https://api.github.com/repos/{text}/contributors"
    results = await asyncio.gather(fetch(URL), fetch(URL2))
    r = results[0]
    r1 = results[1]
    commits = 0
    for developer in r1:
        commits += developer['contributions']
    buttons = InlineKeyboard(row_width=1)
    buttons.add(
        InlineKeyboardButton(
            'Open On Github',
            url=f"https://github.com/{text}"
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
**License:** `{r['license']['name']}`
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
                caption,
                disable_web_page_preview=True
            )
        ))
    return answers


async def tg_search_func(answers, text, user_id):
    if user_id != USERBOT_ID:
        msg = "**ERROR**\n__THIS FEATURE IS ONLY FOR SUDO USERS__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="THIS FEATURE IS ONLY FOR SUDO USERS",
                input_message_content=InputTextMessageContent(msg)
            ))
        return answers
    if str(text)[-1] != ":":
        msg = "**ERROR**\n__Put A ':' After The Text To Search__"
        answers.append(
            InlineQueryResultArticle(
                title="ERROR",
                description="Put A ':' After The Text To Search",
                input_message_content=InputTextMessageContent(msg)
            ))

        return answers
    text = text[0:-1]
    async for message in app2.search_global(text, limit=49):
        buttons = InlineKeyboard(row_width=2)
        buttons.add(
            InlineKeyboardButton(
                text="Origin",
                url=message.link if message.link else "https://t.me/telegram"
            ),
            InlineKeyboardButton(
                text="Search again",
                switch_inline_query_current_chat="search"
            )
        )
        name = message.from_user.first_name if message.from_user.first_name else "NO NAME"
        caption = f"""
**Query:** {text}
**Name:** {str(name)} [`{message.from_user.id}`]
**Chat:** {str(message.chat.title)} [`{message.chat.id}`]
**Date:** {ctime(message.date)}
**Text:** >>

{message.text.markdown if message.text else message.caption if message.caption else "[NO_TEXT]"}
"""
        result = InlineQueryResultArticle(
            title=name,
            description=message.text if message.text else "[NO_TEXT]",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(
                caption,
                disable_web_page_preview=True
                )
        )
        answers.append(result)
    return answers
