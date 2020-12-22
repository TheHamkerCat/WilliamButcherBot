from pyrogram import filters, emoji
from pyrogram.types import Message
from wbb import app

MESSAGE = "{} Welcome {}!"


@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):  # pylint: disable=W0613
    new_members = [i.mention for i in message.new_chat_members]
    text = MESSAGE.format(emoji.CROWN, ",  ".join(new_members))
    await message.reply_text(text, disable_web_page_preview=True)
