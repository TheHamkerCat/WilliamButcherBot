from wbb import app
from wbb.utils.functions import make_carbon
from pyrogram import filters
from wbb.core.decorators.errors import capture_err
import os


__MODULE__ = "Carbon"
__HELP__ = "/carbon - Make Carbon Of Code."


@app.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a text message to make carbon.")
        return
    if not message.reply_to_message.text:
        await message.reply_text("Reply to a text message to make carbon.")
        return
    m = await message.reply_text("Preparing Carbon")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("Uploading")
    await app.send_photo(message.chat.id, carbon)
    await m.delete()
    os.remove(carbon)
