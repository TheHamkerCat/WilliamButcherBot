from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import (blacklist_chat, blacklisted_chats,
                                   whitelist_chat)

__MODULE__ = "Blacklist Chat"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

Use this module to make the bot leave some chats
in which you don't want it to be in.

/blacklist_chat [CHAT_ID] - Blacklist a chat.
/whitelist_chat [CHAT_ID] - Whitelist a chat.
/blacklisted - Show blacklisted chats.
"""


@app.on_message(filters.command("blacklist_chat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("**Usage:**\n/blacklist_chat [CHAT_ID]")
        return
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        await message.reply_text("Chat is already blacklisted.")
        return
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text("Chat has been successfully blacklisted")
        return
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("whitelist_chat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("**Usage:**\n/whitelist_chat [CHAT_ID]")
        return
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        await message.reply_text("Chat is already whitelisted.")
        return
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        await message.reply_text("Chat has been successfully whitelisted")
        return
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("blacklisted_chats") & filters.user(SUDOERS))
async def blacklisted_chats_func(_, message: Message):
    text = ""
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        title = (await app.get_chat(chat_id)).title
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    await message.reply_text(text)
