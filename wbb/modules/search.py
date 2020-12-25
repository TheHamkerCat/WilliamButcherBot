import wikipedia
from search_engine_parser import GoogleSearch
from pyrogram.types import Message
from pyrogram import filters
from requests import get
from wbb import app
from wbb.utils import cust_filter

__MODULE__ = "Search"
__HELP__ = '''/ud - Search For Something In Urban Dictionary
/google - Search For Something On google
/so - Search For Something On StackOverflow
/gh - Search For Something On Github
/wiki - Search For Something On Wikipedia'''

# ud -  urbandictionary


@app.on_message(cust_filter.command(commands=("ud")) & ~filters.edited)
async def urbandict(_, message: Message):
    text = message.text.replace("/ud ", '')
    api = "http://api.urbandictionary.com/v0/define?term="
    if text != '':
        try:
            results = get(f"{api}{text}").json()
            reply_text = f'Definition: {results["list"][0]["definition"]}'
            reply_text += f'\n\nExample: {results["list"][0]["example"]}'
        except IndexError:
            reply_text = ("Sorry could not find any matching results!")
        ignore_chars = "[]"
        reply = reply_text
        for chars in ignore_chars:
            reply = reply.replace(chars, "")
        if len(reply) >= 4096:
            reply = reply[:4096]
        await message.reply_text(reply)

    else:
        await message.reply_text('"/ud" Needs An Argument.')

# google


@app.on_message(cust_filter.command(commands=("google")) & ~filters.edited)
async def google(_, message: Message):
    text = message.text.replace("/google ", '')
    if text != '':
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    else:
        await message.reply_text('"/google" Needs An Argument')

# StackOverflow [This is also a google search with some added args]


@app.on_message(cust_filter.command(commands=("so")) & ~filters.edited)
async def stack(_, message: Message):
    gett = message.text.replace("/so ", '')
    text = gett + ' "site:stackoverflow.com"'
    if gett != '':
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    else:
        await message.reply_text('"/so" Needs An Argument')

# Github [This is also a google search with some added args]


@app.on_message(cust_filter.command(commands=("gh")) & ~filters.edited)
async def github(_, message: Message):
    gett = message.text.replace("/gh ", '')
    text = gett + ' "site:github.com"'
    if gett != '':
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    else:
        await message.reply_text('"/gh" Needs An Argument')

# Wikipedia


@app.on_message(cust_filter.command(commands=("wiki")) & ~filters.edited)
async def wiki(_, message: Message):
    m = message.reply_text('Searching...')
    query = message.text.replace("/wiki", '')
    limit = 5
    if message.reply_to_message:
        query = message.reply_to_message.text
    if not query:
        await message.reply_text('Reply To A Message Or Give An Argument')
        return
    wikipedia.set_lang("en")
    results = wikipedia.search(query)
    output = "```Found These Topics```"
    for i, j in enumerate(results, start=1):
        page = wikipedia.page(j)
        url = page.url
        output += f"[{j}]({url})\n"
        if i == limit:
            break
    await m.delete()
    await message.reply_text(output, disable_web_page_preview=True)
