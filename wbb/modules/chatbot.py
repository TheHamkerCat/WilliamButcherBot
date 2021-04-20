from wbb import app, app2, arq, BOT_ID, SUDOERS, USERBOT_ID, USERBOT_USERNAME
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chatbot_group
from pyrogram import filters


__MODULE__ = "ChatBot"
__HELP__ = """
/chatbot [ON|OFF] To Enable Or Disable ChatBot In Your Chat.
.chatbot [ON|OFF] To Do The Same For Userbot."""

active_chats_bot = []
active_chats_ubot = []


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.edited)
@capture_err
async def chatbot_status(_, message):
    global active_chats_bot
    if len(message.command) != 2:
        await message.reply_text("**Usage**\n/chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats_bot:
            active_chats_bot.append(chat_id)
            text = "Chatbot Enabled Reply To Any Message " \
                   + "Of Mine To Get A Reply"
            await message.reply_text(text)
            return
        await message.reply_text("ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats_bot:
            active_chats_bot.remove(chat_id)
            await message.reply_text("Chatbot Disabled!")
            return
        await message.reply_text("ChatBot Is Already Disabled.")
        return

    else:
        await message.reply_text("**Usage**\n/chatbot [ON|OFF]")


@app.on_message(filters.text & filters.reply & ~filters.bot &
                ~filters.via_bot & ~filters.forwarded, group=chatbot_group)
@capture_err
async def chatbot_talk(_, message):
    if message.chat.id not in active_chats_bot:
        return
    if not message.reply_to_message:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    query = message.text
    luna = await arq.luna(query)
    response = luna.response
    await message.reply_text(response)


""" FOR USERBOT """


@app2.on_message(filters.command("chatbot", prefixes=".") & ~filters.edited & filters.user(SUDOERS))
@capture_err
async def chatbot_status_ubot(_, message):
    global active_chats_ubot
    if len(message.text.split()) != 2:
        await message.edit("**Usage**\n.chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats_ubot:
            active_chats_ubot.append(chat_id)
            text = "Chatbot Enabled Reply To Any Message " \
                   + "Of Mine To Get A Reply"
            await message.edit(text)
            return
        await message.edit("ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats_bot:
            active_chats_bot.remove(chat_id)
            await message.edit("Chatbot Disabled!")
            return
        await message.edit("ChatBot Is Already Disabled.")
        return

    else:
        await message.edit("**Usage**\n/chatbot [ON|OFF]")


@app2.on_message(~filters.me & ~filters.private & filters.text & ~filters.edited, group=chatbot_group)
@capture_err
async def chatbot_talk_ubot(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    username = ("@" + str(USERBOT_USERNAME))
    query = message.text
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != USERBOT_ID and username not in query:
            return
    else:
        if username not in query:
            return
    luna = await arq.luna(query)
    response = luna.response
    await message.reply_text(response)


@app2.on_message(filters.text & filters.private & ~filters.me & ~filters.edited, group=(chatbot_group+1))
@capture_err
async def chatbot_talk_ubot_pm(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    query = message.text
    await app2.send_chat_action(message.chat.id, "typing")
    luna = await arq.luna(query)
    response = luna.response
    await message.reply_text(response)
    await app2.send_chat_action(message.chat.id, "cancel")
