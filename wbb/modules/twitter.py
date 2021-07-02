"""
Twitter Module
"""
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "TwitterSS"
__HELP__ = "/twitterss | .twitterss [Handle] - Take A Screenshot Of A Twitter Profile"


@app.on_message(filters.command("twitterss"))
@capture_err
async def take_ss(_, message):
    try:
        if len(message.command) != 2:
            return await message.reply_text(
                "Give A Handle"
            )
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await app.send_photo(
                message.chat.id,
                photo=f"https://webshot.amanoteam.com/print?q=https://twitter.com/{url}",
            )
        except TypeError:
            return await m.edit("Error")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))
