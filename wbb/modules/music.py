from __future__ import unicode_literals
import youtube_dl
from wbb.utils import cust_filter
from pyrogram import filters
from wbb import app, Command
import os
import glob

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False
}

@app.on_message(cust_filter.command(commands=(["music"])))
async def commit(client, message):
    app.set_parse_mode("markdown")
    await message.reply_chat_action("upload_audio")
    link = (message.text.split(None, 1)[1])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    for filename in glob.glob("*.mp3"):
        filename_final = filename.split("-")[0]+" - "+filename.split("-")[-2]+".mp3"
        os.rename(filename, filename_final)
        m = await message.reply_audio(filename_final)
        await m.edit_caption(f"[{filename_final}]({link})")
        os.remove(filename_final)

