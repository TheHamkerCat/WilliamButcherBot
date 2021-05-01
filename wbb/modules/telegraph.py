# Written by MaskedVirus | github.com/swatv3nub for William and SupMeta_bot
# Kang with Proper Credits
# Part of Pull Req #2 by @MaskedVirus | github.com/swatv3nub

import os
from telegraph import upload_file
from pyrogram import filters
from wbb import app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Telegraph"
__HELP__ = """
Paste Photo and Video to Telegraph
Usage:
/tgphoto - reply to a photo
/tgvideo - reply to a Video
"""


@app.on_message(filters.command("tgphoto"))
@capture_err
async def tgphoto(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a photo.")
        return
    if not message.reply_to_message.photo:
        await message.reply_text("Works only for Photos")
        return
    msg = await message.reply_text("`Uploading to Telegraph...`")
    userid = str(message.chat.id)
    path = (f"./DOWNLOADS/{userid}.jpg")
    path = await client.download_media(message=message.reply_to_message, file_name=path)
    try:
        tlink = upload_file(path)
    except Exception:
        await msg.edit_text("Something went Wrong.")
    else:
        await msg.edit_text(f"Successfully Uploaded to [Telegraph](https://telegra.ph{tlink[0]})")
        os.remove(path)


@app.on_message(filters.command("tgvideo"))
@capture_err
async def tgvideo(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a Video.")
        return
    if not message.reply_to_message.video:
        await message.reply_text("Works only for Videos")
        return
    if(message.video.file_size < 5242880):
        msg = await message.reply_text("Uploading to Telegraph...")
        userid = str(message.chat.id)
        vid_path = (f"./DOWNLOADS/{userid}.mp4")
        vid_path = await client.download_media(message=message.reply_to_message, file_name=vid_path)
        try:
            tlink = upload_file(vid_path)
            await msg.edit_text(f"Successfully Uploaded to [Telegraph](https://telegra.ph{tlink[0]})")
            os.remove(vid_path)
        except Exception:
            await msg.edit_text("Something went Wrong.")
    else:
        await message.reply_text("Size Should Be Less Than 5 mb")
