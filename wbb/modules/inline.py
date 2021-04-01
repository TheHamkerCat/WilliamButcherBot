import sys
from wbb import (
        arq, app, app2, SUDOERS,
        USERBOT_USERNAME, BOT_USERNAME,
        LOG_GROUP_ID)
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch
from pykeyboard import InlineKeyboard
from sys import version as pyver
from motor import version as mongover
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineQueryResultPhoto
)
from googletrans import Translator
from search_engine_parser import GoogleSearch
from time import time

__MODULE__ = "Inline"
__HELP__ = """
tr [LANGUAGE_CODE] [QUERY] - Translate Text.
ud [QUERY] - Urban Dictionary Query.
google [Query] - Google Search.
alive - Check Bot's Stats."""


""" Inspiration From https://github.com/pokurt/Nana-Remix/blob/master/nana/plugins/assistant/inline_mod/alive.py """


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
```{i['descriptions']}```"""
            
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

@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.lower()
        answers = []
        if text == '':
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Click here for help',
                switch_pm_parameter='help',
            )
            return
        elif text.split()[0] == "alive":
            answerss = await alive_function(answers)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
        elif text.split()[0] == "tr":
            lang = text.split()[1]
            tex = text.split(None, 2)[2]
            answerss = await translate_func(answers, lang, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
        elif text.split()[0] == "ud":
            tex = text.split(None, 1)[1]
            answerss = await urban_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
        elif text.split()[0] == "google":
            tex = text.split(None, 1)[1]
            answerss = await google_search_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=10
            )
        elif text.split()[0] == "webss":
            tex = text.split(None, 1)[1]
            answerss = await webss(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

    except IndexError:
        return
