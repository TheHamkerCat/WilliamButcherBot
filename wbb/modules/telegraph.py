from pyrogram import filters
from pyrogram.types import Message

from wbb import app, telegraph
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Telegraph"
__HELP__ = "/telegraph [Page name]: Paste styled text on telegraph."


@app.on_message(filters.command("telegraph"))
@capture_err
async def paste(_, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("Reply to a text message")

    if len(message.command) < 2:
        return await message.reply("**Usage:**\n /telegraph [Page name]")

    page_name = message.text.split(None, 1)[1]
    page = telegraph.create_page(
        page_name, html_content=(reply.text.html).replace("\n", "<br>")
    )
    return await message.reply(
        f"**Posted:** {page['url']}",
        disable_web_page_preview=True,
    )
