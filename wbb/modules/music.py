from __future__ import unicode_literals
from urllib.parse import urlparse
import os
import requests
import youtube_dl
from pyrogram import filters
from pyrogram.types import Message
from wbb.utils import cust_filter
from wbb import app, JSMAPI

__MODULE__ = "Music"
__HELP__ = "/music [link] To Download Music From Various Websites"

ydl_opts = {
    'format': 'bestaudio',
    'writethumbnail': True
}


@app.on_message(cust_filter.command(commands=("music")) & ~filters.edited)
async def music(_, message: Message):
    await message.reply_chat_action("typing")
    app.set_parse_mode("html")
    try:
        link = (message.text.split(None, 1)[1])
    except IndexError:
        await message.reply_text(
            "<code>\"/music\" needs a keyword argument</code>")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
        # .webm -> .weba
        basename = audio_file.rsplit(".", 1)[-2]
        thumbnail_url = info_dict['thumbnail']
        thumbnail_file = basename + "." + \
            get_file_extension_from_url(thumbnail_url)
        if info_dict['ext'] == 'webm':
            audio_file_weba = basename + ".weba"
            os.rename(audio_file, audio_file_weba)
            audio_file = audio_file_weba
        # info
        title = info_dict['title']
        webpage_url = info_dict['webpage_url']
        performer = info_dict['uploader']
        duration = int(float(info_dict['duration']))
        caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
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

# Song


@app.on_message(cust_filter.command(commands=("song")) & ~filters.edited)
async def song(_, message: Message):
    text = message.text.replace("/song ", "")
    query = text.replace(" ", "%20")
    r = requests.get(f"{JSMAPI}{query}")
    import wget
    import os
    i = 0
    while i < 2:
        sname = r.json()[i]['song']
        slink = r.json()[i]['media_url']
        ssingers = r.json()[i]['singers']
        sduration = r.json()[i]['duration']
        file = wget.download(slink)
        ffile = file.replace("mp4", "m4a")
        os.rename(file, ffile)
        await message.reply_audio(audio=ffile, title=sname,
                                  performer=ssingers, duration=int(sduration))
        i += 1
        os.remove(ffile)
