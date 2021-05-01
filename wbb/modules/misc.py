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
import secrets
import string
import aiohttp
from pyrogram import filters
from googletrans import Translator
from cryptography.fernet import Fernet
from wbb import app, FERNET_ENCRYPTION_KEY
from wbb.utils import random_line
from wbb.utils.json_prettify import json_prettify
from wbb.utils.fetch import fetch
from wbb.utils.pastebin import paste
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Misc"
__HELP__ = '''/commit - Generate Funny Commit Messages
/runs  - Idk Test Yourself
/id - Get Chat_ID or User_ID
/random [Length] - Generate Random Complex Passwords
/encrypt - Encrypt Text [Can Only Be Decrypted By This Bot]
/decrypt - Decrypt Text
/cheat [Language] [Query] - Get Programming Related Help
/weather [City] - To Get Weather Info
/tr [en] - Translate A Message
/json [URL] - Get Response From An API or Something.
#RTFM - Check it lol'''


@app.on_message(filters.command("commit") & ~filters.edited)
async def commit(_, message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(filters.command("RTFM", "#"))
async def rtfm(_, message):
    await message.delete()
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message lol")
        return
    await message.reply_to_message.reply_text("Are You Lost? READ THE FUCKING DOCS!")


@app.on_message(filters.command("runs") & ~filters.edited)
async def runs(_, message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(filters.command("id"))
async def getid(_, message):
    if len(message.command) == 2:
        id = (await app.get_users(message.text.split(None, 1)[1])).id
        text = f"<b>ID:</b> {id}"
        return
    text_unping = "<b>Chat ID:</b>"
    if message.chat.username:
        text_unping = (
            f'<a href="https://t.me/{message.chat.username}">{text_unping}</a>'
        )
    text_unping += f" <code>{message.chat.id}</code>\n"
    text = "<b>Message ID:</b>"
    if message.link:
        text = f'<a href="{message.link}">{text}</a>'
    text += f" <code>{message.message_id}</code>\n"
    text_unping += text
    if message.from_user:
        text_unping += f'<b><a href="tg://user?id={message.from_user.id}">User ID:</a></b> <code>{message.from_user.id}</code>\n'
    text_ping = text_unping
    reply = message.reply_to_message
    if not getattr(reply, "empty", True):
        text_unping += "\n"
        text = "<b>Replied Message ID:</b>"
        if reply.link:
            text = f'<a href="{reply.link}">{text}</a>'
        text += f" <code>{reply.message_id}</code>\n"
        text_unping += text
        text_ping = text_unping
        if reply.from_user:
            text = "<b>Replied User ID:</b>"
            if reply.from_user.username:
                text = f'<a href="https://t.me/{reply.from_user.username}">{text}</a>'
            text += f" <code>{reply.from_user.id}</code>\n"
            text_unping += text
            text_ping += f'<b><a href="tg://user?id={reply.from_user.id}">Replied User ID:</a></b> <code>{reply.from_user.id}</code>\n'
        if reply.forward_from:
            text_unping += "\n"
            text = "<b>Forwarded User ID:</b>"
            if reply.forward_from.username:
                text = (
                    f'<a href="https://t.me/{reply.forward_from.username}">{text}</a>'
                )
            text += f" <code>{reply.forward_from.id}</code>\n"
            text_unping += text
            text_ping += f'\n<b><a href="tg://user?id={reply.forward_from.id}">Forwarded User ID:</a></b> <code>{reply.forward_from.id}</code>\n'
    reply = await message.reply_text(text_unping, disable_web_page_preview=True)
    if text_unping != text_ping:
        await reply.edit_text(text_ping, disable_web_page_preview=True)

# Random


@app.on_message(filters.command('random') & ~filters.edited)
@capture_err
async def random(_, message):
    if len(message.command) != 2:
        await message.reply_text('"/random" Needs An Argurment.'
                                 ' Ex: `/random 5`')
        return
    length = message.text.split(None, 1)[1]

    try:
        if 1 < int(length) < 1000:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in
                               range(int(length)))
            await message.reply_text(f"`{password}`")
        else:
            await message.reply_text('Specify A Length Between 1-1000')
    except ValueError:
        await message.reply_text("Strings Won't Work!, Pass A"
                                 + " Positive Integer Between 1-1000")

# Encrypt


@app.on_message(filters.command('encrypt') & ~filters.edited)
@capture_err
async def encrypt(_, message):
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Encrypt It.')
        return
    text = message.reply_to_message.text
    text_in_bytes = bytes(text, 'utf-8')
    cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
    encrypted_text = cipher_suite.encrypt(text_in_bytes)
    bytes_in_text = encrypted_text.decode("utf-8")
    await message.reply_text(bytes_in_text)

# Decrypt


@app.on_message(filters.command('decrypt') & ~filters.edited)
@capture_err
async def decrypt(_, message):
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Decrypt It.')
        return
    text = message.reply_to_message.text
    text_in_bytes = bytes(text, 'utf-8')
    cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
    decoded_text = cipher_suite.decrypt(text_in_bytes)
    bytes_in_text = decoded_text.decode("utf-8")
    await message.reply_text(bytes_in_text)


async def fetch_text(url):
    async with aiohttp.ClientSession(headers={"user-agent": "curl"}) as session:
        async with session.get(url) as resp:
            data = await resp.text()
    return data


# Cheat.sh


@app.on_message(filters.command("cheat") & ~filters.edited)
@capture_err
async def cheat(_, message):
    if len(message.command) < 3:
        await message.reply_text("/cheat [language] [query]")
        return
    text = message.text.split(None, 1)[1]
    m = await message.reply_text("Searching")
    try:
        ftext = text.split()
        language = ftext[0]
        query = ftext[1]
        data = await fetch_text(f"http://cht.sh/{language}/{query}?QT")
        if not data:
            await m.edit("Found Literally Nothing!")
            return
        await m.edit(f"`{data}`")
    except Exception as e:
        await m.edit(str(e))
        print(str(e))

# Weather


@app.on_message(filters.command("weather") & ~filters.edited)
@capture_err
async def weather(_, message):
    if len(message.command) != 2:
        await message.reply_text("/weather [city]")
        return
    city = message.text.split(None, 1)[1]
    m = await message.reply_text("Fetching Data")
    data = await fetch_text(f"https://wttr.in/{city}?mnTC0")
    await m.edit(f"`{data}`")

# Translate


@app.on_message(filters.command("tr") & ~filters.edited)
@capture_err
async def tr(_, message):
    if len(message.command) != 2:
        await message.reply_text("/tr [LANGUAGE_CODE]")
        return
    lang = message.text.split(None, 1)[1]
    if not message.reply_to_message or not lang:
        await message.reply_text(
            "Reply to a message with /tr [language code]"
            + "\nGet supported language list from here -"
            + " https://py-googletrans.readthedocs.io/en"
            + "/latest/#googletrans-languages"
        )
        return
    if message.reply_to_message.text:
        text = message.reply_to_message.text
        try:
            i = Translator().translate(text, dest=lang)
        except ValueError:
            await message.reply_text("[ERROR]: LANGUAGE NOT FOUND")
            return
        await message.reply_text(i.text)
    elif message.reply_to_message.caption:
        text = message.reply_to_message.caption
        i = Translator().translate(text, dest=lang)
        await message.reply_text(i.text)


fetch_limit = 0


@app.on_message(filters.command("json") & ~filters.edited)
@capture_err
async def json_fetch(_, message):
    global fetch_limit
    if len(message.command) != 2:
        await message.reply_text("/json [URL]")
        return
    elif fetch_limit > 500:
        await message.reply_text("Today's Quota Exceeded!, lol")
        return
    url = message.text.split(None, 1)[1]
    try:
        data = await fetch(url)
        data = await json_prettify(data)
        fetch_limit += 1
        if len(data) < 4090:
            await message.reply_text(data)
        else:
            link = await paste(data)
            await message.reply_text(f"[OUTPUT_TOO_LONG]({link})", disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))


@app.on_message(filters.command('bun'))
async def bunn(_, message):
    if message.reply_to_message:
        await message.reply_to_message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")
        return
    if not message.reply_to_message:
        await message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")
