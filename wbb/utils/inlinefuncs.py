from wbb import (
        arq, app, app2, USERBOT_USERNAME,
        BOT_USERNAME, LOG_GROUP_ID )
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineQueryResultPhoto
)
from googletrans import Translator
from search_engine_parser import GoogleSearch
from time import time
from wbb.utils.fetch import fetch
from pykeyboard import InlineKeyboard
from sys import version as pyver
import sys
from motor import version as mongover
from pyrogram import __version__ as pyrover
import aiohttp
import json

async def alive_function(answers):
    buttons = InlineKeyboard(row_width=1)
    bot_state = 'Dead' if not await app.get_me() else 'Alive'
    ubot_state = 'Dead' if not await app2.get_me() else 'Alive'
    buttons.add(InlineKeyboardButton('Stats', callback_data='stats_callback'))
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
    for i in results:
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
    for i in gresults:
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


async def webss(url):
    start_time = time()
    if "." not in url:
        return
    screenshot = await fetch(f"https://patheticprogrammers.cf/ss?site={url}")
    end_time = time()
    m = await app.send_photo(LOG_GROUP_ID, photo=screenshot['url'])
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
        input_message_content=InputTextMessageContent(msg, disable_web_page_preview=True)
    )
    a.append(b)
    return a
