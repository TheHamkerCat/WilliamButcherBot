from youtube_search import YoutubeSearch
from search_engine_parser import GoogleSearch
from pyrogram.types import Message
from pyrogram import filters
from requests import get
from wbb import app
from wbb.utils import cust_filter
from wbb.utils.errors import capture_err

__MODULE__ = "Search"
__HELP__ = '''/ud - Search For Something In Urban Dictionary
/google - Search For Something On Google
/yt - Search For Something On YouTube'''

# ud -  urbandictionary


@app.on_message(cust_filter.command(commands=("ud")) & ~filters.edited)
@capture_err
async def urbandict(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text('"/ud" Needs An Argument.')
        return
    text = message.text.split(None, 1)[1]
    api = "http://api.urbandictionary.com/v0/define?term="

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

# google


@app.on_message(cust_filter.command(commands=("google")) & ~filters.edited)
@capture_err
async def google(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text('"/google" Needs An Argument')
            return
        text = message.text.split(None, 1)[1]
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
    except Exception as e:
        await message.reply_text(str(e))


# StackOverflow [This is also a google search with some added args]


@app.on_message(cust_filter.command(commands=("so")) & ~filters.edited)
@capture_err
async def stack(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text('"/so" Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:stackoverflow.com"'
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
    except Exception as e:
        await message.reply_text(str(e))


# Github [This is also a google search with some added args]


@app.on_message(cust_filter.command(commands=("gh")) & ~filters.edited)
@capture_err
async def github(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text('"/gh" Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:github.com"'
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
    except Exception as e:
        await message.reply_text(str(e))


# YouTube


@app.on_message(cust_filter.command(commands=("yt")) & ~filters.edited)
@capture_err
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/yt needs an argument")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("Searching....")
        results = YoutubeSearch(query, max_results=4).to_dict()
        i = 0
        text = ""
        while i < 4:
            text += f"Title - {results[i]['title']}\n"
            text += f"Duration - {results[i]['duration']}\n"
            text += f"Views - {results[i]['views']}\n"
            text += f"Channel - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
