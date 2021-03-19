from pyrogram import filters
from wbb import app
from wbb.utils.errors import capture_err

__MODULE__ = "Stickers"
__HELP__ = """/sticker_id - To Get File ID of A Sticker."""

## TODO Need to add /kang here

@app.on_message(filters.command("sticker_id") & ~filters.edited)
async def sticker_id(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a sticker.")
        return
    if not message.reply_to_message.sticker:
        await message.reply_text("Reply to a sticker.")
        return
    file_id = message.reply_to_message.sticker.file_id
    await message.reply_text(f"`{file_id}`")

