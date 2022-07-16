from asyncio import sleep
from pyrogram import filters
from pyrogram.types import Message
from telegraph.exceptions import RetryAfterError

from wbb import app, telegraph
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Telegraph"
__HELP__ = "/telegraph [Page name]: Paste styled text on telegraph."

async def create_telegraph(title: str, content: str) -> str:
    try:
        return await telegraph.create_page(
            title, html_content=content.replace("\n", "<br>")
        )
    except RetryAfterError as e:
        await sleep(st.retry_after)
        return await create_telegraph(title=title, content=content)

@app.on_message(filters.command("telegraph") & ~filters.edited)
@capture_err
async def paste(_, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("Reply to a text message")

    if len(message.command) < 2:
        return await message.reply("**Usage:**\n /telegraph [Page name]")
    
    page_name = message.text.split(None, 1)[1]
    page = await create_telegraph(
        title=page_name, content=reply.text.html
    )
    return await message.reply(
        f"**Posted:** {page['url']}",
        disable_web_page_preview=True,
    )
