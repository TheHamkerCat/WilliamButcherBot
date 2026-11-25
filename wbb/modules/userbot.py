from pyrogram import filters
from pyrogram.types import Message

from wbb import app2  # don't remove
from wbb import SUDOERS, USERBOT_PREFIX, eor


@app2.on_message(
    filters.command("reserve", prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & SUDOERS
)
async def reserve_channel_handler(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(message, text="Pass a username as argument!!")

    username = message.text.split(None, 1)[1].strip().replace("@", "")

    m = await eor(message, text="Reserving...")

    chat = await app2.create_channel(username, "Created by .reserve command")
    try:
        await app2.set_chat_username(chat.id, username)
    except Exception as e:
        await m.edit(f"Couldn't Reserve, Error: `{str(e)}`")
        return await app2.delete_channel(chat.id)
    await m.edit(f"Reserved @{username} Successfully")
