"""
ImageSS
"""
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "ImageSS"
__HELP__ = "/imagess | .imagess [Query] - Take A Screenshot Of A Google Image Search"


@app.on_message(filters.command("imagess"))
@capture_err
async def take_ss(_, message):
    async def take_ss(_, message):
    try:
        if len(message.command) != 2:
            return await message.reply_text(
                "Invalid. If your query contains a space please replace it with a plus sign. Like if your query is Disney Movies, write Disney+Movies"
            )
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await app.send_photo(
                message.chat.id,
                photo=f"https://webshot.amanoteam.com/print?q=https://www.google.com/search?tbm=isch&q={url}",
            )
        except TypeError:
            return await m.edit("Error")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))