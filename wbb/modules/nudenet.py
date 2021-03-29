from wbb import app
from pyrogram import filters
from wbb.utils.errors import capture_err
from nudenet import NudeDetector
import os

detector = NudeDetector()


@app.on_message(filters.photo & filters.sticker & filters.document)
async def nudenet_detector(_, message):
    if message.document:
        if message.document.mime_type != "image/png" and \
                message.document.mime_type != "image/jpg" and \
                message.document.mime_type != "image/jpeg":
                    return
    mention = message.from_user.mention
    file = await message.download()
    image = detector.detect(file, mode='fast')
    if image:
        try:
            await message.delete()
        except Exception:
            await message.reply_text("It's a NSFW image, If i had enough permissions, I would've deleted it")
            os.remove(file)
            return
    await message.reply_text(f"{mention} Sent a NSFW image, so i deleted it.")
    os.remove(f)
            
