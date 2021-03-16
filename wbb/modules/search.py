from search_engine_parser import GoogleSearch
from pyrogram import filters
from wbb import app, arq
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch

__MODULE__ = "Search"
__HELP__ = '''/ud - Search For Something In Urban Dictionary
/google - Search For Something On Google
/so - Search For Something On Stack OverFlow
/gh - Search For Something On GitHub
/yt - Search For Something On YouTube'''

# ud -  urbandictionary


@app.on_message(filters.command("ud") & ~filters.edited)
@capture_err
async def urbandict(_, message):
    if len(message.command) < 2:
        await message.reply_text('"/ud" Needs An Argument.')
        return
    text = message.text.split(None, 1)[1]
    try:
        results = await arq.urbandict(text, 1)
        reply_text = f"""**Definition:** __{results[0].definition}__

**Example:** __{results[0].example}__"""
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


@app.on_message(filters.command("google") & ~filters.edited)
@capture_err
async def google(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text('/google Needs An Argument')
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


@app.on_message(filters.command("so") & ~filters.edited)
@capture_err
async def stack(_, message):
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


@app.on_message(filters.command("gh") & ~filters.edited)
@capture_err
async def github(_, message):
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


@app.on_message(filters.command("yt") & ~filters.edited)
@capture_err
async def ytsearch(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/yt needs an argument")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("Searching....")
        results = await arq.youtube(query, 3)
        i = 0
        text = ""
        while i < 3:
            text += f"Title - {results[i].title}\n"
            text += f"Duration - {results[i].duration}\n"
            text += f"Views - {results[i].views}\n"
            text += f"Channel - {results[i].channel}\n"
            text += f"https://youtube.com{results[i].url_suffix}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
