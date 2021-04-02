import sys
from wbb import app
from wbb.utils.inlinefuncs import (
        google_search_func, urban_func, translate_func,
        alive_function, webss, shortify
        )
from pyrogram import filters

__MODULE__ = "Inline"
__HELP__ = """
tr [LANGUAGE_CODE] [QUERY] - Translate Text.
ud [QUERY] - Urban Dictionary Query.
google [Query] - Google Search.
alive - Check Bot's Stats.
webss [URL] - Take A Screenshot Of A Website.
bitly [URL] - Shorten A Link"""


""" Inspiration From https://github.com/pokurt/Nana-Remix/blob/master/nana/plugins/assistant/inline_mod/alive.py """

@app.on_message(filters.command("inline"))
async def inline_help(_, message):
    await app.send_message(message.chat.id, text=__HELP__)


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
                switch_pm_parameter='inline',
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
        elif text.split()[0] == "bitly":
            tex = text.split(None, 1)[1]
            answerss = await shortify(tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
                cache_time=2
            )

    except (IndexError, TypeError) as e:
        return
