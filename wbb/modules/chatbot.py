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
from asyncio import sleep, gather
from pyrogram import filters
from pyrogram.types import Message

from wbb import (BOT_ID, SUDOERS, USERBOT_ID, USERBOT_PREFIX, USERBOT_USERNAME,
                 app, app2, arq)
from wbb.core.decorators.errors import capture_err
from wbb.modules.userbot import edit_or_reply
from wbb.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot"
__HELP__ = """
/chatbot [ON|OFF] To Enable Or Disable ChatBot In Your Chat.
.chatbot [ON|OFF] To Do The Same For Userbot."""

active_chats_bot = []
active_chats_ubot = []

async def chat_bot_toggle(db, message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = (
                "Chatbot Enabled Reply To Any Message "
                + "Of Mine To Get A Reply"
            )
            return await edit_or_reply(message, text=text)
        await edit_or_reply(message, text="ChatBot Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await edit_or_reply(message, text="Chatbot Disabled!")
        await edit_or_reply(message, text="ChatBot Is Already Disabled.")
    else:
        await edit_or_reply(message, text="**Usage**\n/chatbot [ON|OFF]")

# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.edited)
@capture_err
async def chatbot_status(_, message):
    if len(message.command) != 2:
        return await edit_or_reply(message, text="**Usage**\n/chatbot [ON|OFF]")
    await chat_bot_toggle(active_chats_bot, message)

async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result

async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")

@app.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message):
    if message.chat.id not in active_chats_bot:
        return
    if not message.reply_to_message:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    await type_and_send(message)


""" FOR USERBOT """


@app2.on_message(
    filters.command("chatbot", prefixes=USERBOT_PREFIX)
    & ~filters.edited
    & filters.user(SUDOERS)
)
@capture_err
async def chatbot_status_ubot(_, message):
    if len(message.text.split()) != 2:
        return await edit_or_reply(
            message, text="**Usage**\n.chatbot [ON|OFF]"
        )
    await chat_bot_toggle(active_chats_ubot, message)


@app2.on_message(
    ~filters.me & ~filters.private & filters.text & ~filters.edited,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk_ubot(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    username = "@" + str(USERBOT_USERNAME)
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        if (
            message.reply_to_message.from_user.id != USERBOT_ID
            and username not in message.text
        ):
            return
    else:
        if username not in message.text:
            return
    await type_and_send(message)


@app2.on_message(
    filters.text & filters.private & ~filters.me & ~filters.edited,
    group=(chatbot_group + 1),
)
@capture_err
async def chatbot_talk_ubot_pm(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    await type_and_send(message)
