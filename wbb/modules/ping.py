from pyrogram import filters
from wbb import app

__MODULE__ = "Ping"
__HELP__ = " /ping - To Check If Bot Is Alive"


@app.on_message(filters.command("ping") & ~filters.edited)
async def ping(_, message):
    await message.reply_text("Alive!")
