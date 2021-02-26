from wbb import app, LOG_GROUP_ID
from wbb.utils.json_prettify import json_object_prettify
from wbb.utils.errors import capture_err
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from pyrogram import filters


__MODULE__ = "Advanced"
__HELP__ = """**NOTE** - Some of these commands are only supported in BOT_LOG_GROUP [OWNER]
/get_chat [CHAT_ID] - Get Info of A Chat.
/get_user [USER_ID] - Get Info of A User.
/leave_chat [CHAT_ID] - Leave The Chat.
/send_message [CHAT_ID] [TEXT] - Send A Message To A Chat."""


@app.on_message(filters.command("get_chat") & ~filters.edited)
@capture_err
async def get_chat_data(_, message):
    if len(message.command) != 2:
        await message.reply_text("/get_chat [CHAT_ID]")
        return
    try:
        chat_id = message.text.split(None, 1)[1]
        chat_data = await app.get_chat(chat_id)
        data = await json_object_prettify(chat_data)
        await app.send_message(message.chat.id, data)
    except (PeerIdInvalid, ChannelInvalid) as e:
        await message.reply_text("PEER_ID_INVALID")
        print(str(e))


@app.on_message(filters.command("get_user") & ~filters.edited)
@capture_err
async def get_user_data(_, message):
    if len(message.command) != 2:
        await message.reply_text("/get_user [USER_ID]")
        return
    try:
        user_id = message.text.split(None, 1)[1]
        user_data = await app.get_users(user_id)
        data = await json_object_prettify(user_data)
        await app.send_message(message.chat.id, data)
    except (PeerIdInvalid, ChannelInvalid) as e:
        await message.reply_text("PEER_ID_INVALID")
        print(str(e))


@app.on_message(filters.command("leave_chat") & ~filters.edited & filters.chat(LOG_GROUP_ID))
@capture_err
async def leave_chat(_, message):
    if len(message.command) != 2:
        await message.reply_text("/leave_chat [CHAT_ID]")
        return
    try:
        chat_id = message.text.split(None, 1)[1]
        await app.leave_chat(chat_id)
        await message.reply_text("Left The Chat!")
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))


@app.on_message(filters.command("send_message") & ~filters.edited & filters.chat(LOG_GROUP_ID))
@capture_err
async def send_message(_, message):
    if len(message.command) < 3:
        await message.reply_text("/send_message [CHAT_ID] [TEXT]")
        return
    try:
        chat_id = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        await app.send_message(chat_id, text=text)
        await message.reply_text("Message Sent!")
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))
