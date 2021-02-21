from __future__ import unicode_literals
from urllib.parse import urlparse
import os
import youtube_dl
import aiohttp
import json
import wget
from pyrogram import filters
from pyrogram.types import Message
from wbb.utils import cust_filter
from wbb import app, OWNER_ID, SUDO_USER_ID

SUDOERS = [OWNER_ID, SUDO_USER_ID]

__MODULE__ = "Music"
__HELP__ = "/music [link] To Download Music From Various Websites"

ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}


@app.on_message(cust_filter.command(commands=("music")) & ~filters.edited & filters.user(SUDOERS))
async def music(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("`/music` needs a link as argument")
        return
    link = message.text.split(None, 1)[1]
    m = await message.reply_text(f"Downloading {link}",
                                 disable_web_page_preview=True)
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
            # .webm -> .weba
            basename = audio_file.rsplit(".", 1)[-2]
            thumbnail_url = info_dict['thumbnail']
            thumbnail_file = basename + "." + get_file_extension_from_url(thumbnail_url)
            audio_file = basename + ".mp3"
    except Exception as e:
        await m.edit(str(e))
        return
        # info
    title = info_dict['title']
    webpage_url = info_dict['webpage_url']
    performer = info_dict['uploader']
    duration = int(float(info_dict['duration']))
    caption = f"[{title}]({webpage_url})"
    await m.delete()
    await message.reply_chat_action("upload_document")
    await message.reply_audio(audio_file, caption=caption,
                              duration=duration, performer=performer,
                              title=title, thumb=thumbnail_file)
    os.remove(audio_file)
    os.remove(thumbnail_file)


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]
