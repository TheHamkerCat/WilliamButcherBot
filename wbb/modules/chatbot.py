"""
MIT License

Copyright (c) 2024 TheHamkerCat

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
from asyncio import gather, sleep

from pyrogram import enums, filters
from pyrogram.types import Message

from wbb import BOT_ID, app, arq, eor
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.utils.dbfunctions import add_chatbot, check_chatbot, rm_chatbot
from wbb.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot"
__HELP__ = """
/chatbot [ENABLE|DISABLE] To Enable Or Disable ChatBot In Your Chat.
"""


async def chat_bot_toggle(message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    db = (await check_chatbot())["bot"]
    if status == "enable":
        if chat_id not in db:
            await add_chatbot(chat_id)
            text = "Chatbot Enabled!"
            return await eor(message, text=text)
        await eor(message, text="ChatBot Is Already Enabled.")
    elif status == "disable":
        if chat_id in db:
            await rm_chatbot(chat_id)
            return await eor(message, text="Chatbot Disabled!")
        await eor(message, text="ChatBot Is Already Disabled.")
    else:
        await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.private)
@adminsOnly("can_change_info")
@capture_err
async def chatbot_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")
    await chat_bot_toggle(message)


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, enums.ChatAction.CANCEL)


@app.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["bot"]:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    await type_and_send(message)
