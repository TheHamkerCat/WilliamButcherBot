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
from asyncio import Lock

from pyrogram import filters

from wbb import SUDOERS, USERBOT_PREFIX, app, app2, arq, eor
from wbb.core.decorators.errors import capture_err
from wbb.utils import random_line
from wbb.utils.http import get
from wbb.utils.json_prettify import json_prettify
from wbb.utils.pastebin import paste

__MODULE__ = "Misc"
__HELP__ = """
/asq
    Ask a question

/commit
    Generate Funny Commit Messages

/runs
    Idk Test Yourself

/id
    Get Chat_ID or User_ID

/random [Length]
    Generate Random Complex Passwords

/cheat [Language] [Query]
    Get Programming Related Help

/tr [LANGUAGE_CODE]
    Translate A Message
    Ex: /tr en

/json [URL]
    Get parsed JSON response from a rest API.

/arq
    Statistics Of ARQ API.

/webss [URL]
    Take A Screenshot Of A Webpage

/reverse
    Reverse search an image.

/carbon
    Make Carbon from code.

/tts
    Convert Text To Speech.

/autocorrect [Reply to a message]
    Autocorrects the text in replied message.

/pdf [Reply to an image (as document) or a group of images.]
    Convert images to PDF, helpful for online classes.

/markdownhelp
    Sends mark down and formatting help.

/backup
    Backup database

#RTFM - Tell noobs to read the manual
"""

ASQ_LOCK = Lock()


@app.on_message(filters.command("asq") & ~filters.edited)
async def asq(_, message):
    err = "Reply to text message or pass the question as argument"
    if message.reply_to_message:
        if not message.reply_to_message.text:
            return await message.reply(err)
        question = message.reply_to_message.text
    else:
        if len(message.command) < 2:
            return await message.reply(err)
        question = message.text.split(None, 1)[1]
    m = await message.reply("Thinking...")
    async with ASQ_LOCK:
        resp = await arq.asq(question)
        await m.edit(resp.result)


@app.on_message(filters.command("commit") & ~filters.edited)
async def commit(_, message):
    await message.reply_text(await get("http://whatthecommit.com/index.txt"))


@app.on_message(filters.command("RTFM", "#"))
async def rtfm(_, message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message lol")
    await message.reply_to_message.reply_text(
        "Are You Lost? READ THE FUCKING DOCS!"
    )


@app.on_message(filters.command("runs") & ~filters.edited)
async def runs(_, message):
    await message.reply_text((await random_line("wbb/utils/runs.txt")))


@app2.on_message(
    filters.command("id", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
@app.on_message(filters.command("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.message_id
    reply = message.reply_to_message

    text = f"**[Message ID:]({message.link})** `{message_id}`\n"
    text += f"**[Your ID:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[User ID:](tg://user?id={user_id})** `{user_id}`\n"
        except Exception:
            return await eor(message, text="This user doesn't exist.")

    text += f"**[Chat ID:](https://t.me/{chat.username})** `{chat.id}`\n\n"
    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += (
            f"**[Replied Message ID:]({reply.link})** `{reply.message_id}`\n"
        )
        text += f"**[Replied User ID:](tg://user?id={id_})** `{id_}`"

    await eor(
        message,
        text=text,
        disable_web_page_preview=True,
        parse_mode="md",
    )


# Random
@app.on_message(filters.command("random") & ~filters.edited)
@capture_err
async def random(_, message):
    if len(message.command) != 2:
        return await message.reply_text(
            '"/random" Needs An Argurment.' " Ex: `/random 5`"
        )
    length = message.text.split(None, 1)[1]
    try:
        if 1 < int(length) < 1000:
            alphabet = string.ascii_letters + string.digits
            password = "".join(
                secrets.choice(alphabet) for i in range(int(length))
            )
            await message.reply_text(f"`{password}`")
        else:
            await message.reply_text("Specify A Length Between 1-1000")
    except ValueError:
        await message.reply_text(
            "Strings Won't Work!, Pass A Positive Integer Less Than 1000"
        )


# Translate
@app.on_message(filters.command("tr") & ~filters.edited)
@capture_err
async def tr(_, message):
    if len(message.command) != 2:
        return await message.reply_text("/tr [LANGUAGE_CODE]")
    lang = message.text.split(None, 1)[1]
    if not message.reply_to_message or not lang:
        return await message.reply_text(
            "Reply to a message with /tr [language code]"
            + "\nGet supported language list from here -"
            + " https://py-googletrans.readthedocs.io/en"
            + "/latest/#googletrans-languages"
        )
    reply = message.reply_to_message
    text = reply.text or reply.caption
    if not text:
        return await message.reply_text("Reply to a text to translate it")
    result = await arq.translate(text, lang)
    if not result.ok:
        return await message.reply_text(result.result)
    await message.reply_text(result.result.translatedText)


@app.on_message(filters.command("json") & ~filters.edited)
@capture_err
async def json_fetch(_, message):
    if len(message.command) != 2:
        return await message.reply_text("/json [URL]")
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("Fetching")
    try:
        data = await get(url)
        data = await json_prettify(data)
        if len(data) < 4090:
            await m.edit(data)
        else:
            link = await paste(data)
            await m.edit(
                f"[OUTPUT_TOO_LONG]({link})",
                disable_web_page_preview=True,
            )
    except Exception as e:
        await m.edit(str(e))


@app.on_message(filters.command("webss"))
@capture_err
async def take_ss(_, message):
    if len(message.command) != 2:
        return await message.reply_text("Give A Url To Fetch Screenshot.")
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("**Uploading**")
    try:
        await app.send_photo(
            message.chat.id,
            photo=f"https://webshot.amanoteam.com/print?q={url}",
        )
    except Exception:
        return await m.edit("No Such Website.")
    await m.delete()


@app.on_message(filters.command(["kickme", "banme"]))
async def kickbanme(_, message):
    await message.reply_text(
        "Haha, it doesn't work that way, You're stuck with everyone here."
    )
