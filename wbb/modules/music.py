"""
MIT License

Copyright (c) 2024 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
import shutil
import tempfile
from asyncio import get_running_loop
from functools import partial
from io import BytesIO

import yt_dlp
from pyrogram import filters

from wbb import SUDOERS, aiohttpsession as session
from wbb import app, arq
from wbb.core.decorators.errors import capture_err
from wbb.utils.pastebin import paste

__MODULE__ = "Music"
__HELP__ = """
/ytmusic [link] To Download Music From Various Websites Including Youtube. [SUDOERS]
/saavn [query] To Download Music From Saavn.
/lyrics [query] To Get Lyrics Of A Song.
"""

is_downloading = False


def reserve_download() -> bool:
    global is_downloading
    if is_downloading:
        return False
    is_downloading = True
    return True


def release_download():
    global is_downloading
    is_downloading = False


def download_youtube_audio(query):
    # Prefix bare search terms with ytsearch1: so yt-dlp resolves them.
    is_url = query.startswith("http://") or query.startswith("https://")
    target = query if is_url else f"ytsearch1:{query}"
    temp_dir = tempfile.mkdtemp(prefix="wbb-yt-")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "writethumbnail": True,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": 50 * 1024 * 1024,
        "cachedir": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target, download=True)
            # For search results yt-dlp wraps entries in a playlist dict.
            if "entries" in info:
                info = info["entries"][0]

            duration = int(info.get("duration") or 0)
            if duration > 1800:
                shutil.rmtree(temp_dir, ignore_errors=True)
                return None

            title = info.get("title", "Unknown")
            performer = info.get("uploader") or info.get("channel", "Unknown")
            # Sanitize ID to prevent path traversal.
            safe_id = re.sub(r"[^\w\-]", "_", info["id"])
            audio_file = os.path.join(temp_dir, f"{safe_id}.mp3")
            # yt-dlp writes the thumbnail as <id>.<ext>; find whatever it wrote.
            thumbnail_file = next(
                (
                    os.path.join(temp_dir, f"{safe_id}.{ext}")
                    for ext in ("webp", "jpg", "png")
                    if os.path.exists(
                        os.path.join(temp_dir, f"{safe_id}.{ext}")
                    )
                ),
                None,
            )

        return [
            title,
            performer,
            duration,
            audio_file,
            thumbnail_file,
            temp_dir,
        ]
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


@app.on_message(filters.command("ytmusic") & SUDOERS)
@capture_err
async def music(_, message):
    if len(message.command) < 2:
        return await message.reply_text("/ytmusic needs a query as argument")

    url = message.text.split(None, 1)[1]
    if not reserve_download():
        return await message.reply_text(
            "Another download is in progress, try again after sometime."
        )
    m = None
    temp_dir = None
    try:
        m = await message.reply_text(
            f"Downloading {url}", disable_web_page_preview=True
        )
        loop = get_running_loop()
        music = await loop.run_in_executor(
            None, partial(download_youtube_audio, url)
        )

        if not music:
            return await message.reply_text("[ERROR]: MUSIC TOO LONG")
        (
            title,
            performer,
            duration,
            audio_file,
            thumbnail_file,
            temp_dir,
        ) = music
        await message.reply_audio(
            audio_file,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumbnail_file,
        )
        await m.delete()
    except Exception as e:
        if m:
            return await m.edit(str(e))
        return await message.reply_text(str(e))
    finally:
        release_download()
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)


async def download_song(url):
    async with session.get(url) as resp:
        song = await resp.read()
    song = BytesIO(song)
    song.name = "a.mp3"
    return song


# Lyrics


@app.on_message(filters.command("lyrics"))
async def lyrics_func(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n/lyrics [QUERY]")
    m = await message.reply_text("**Searching**")
    query = message.text.strip().split(None, 1)[1]

    resp = await arq.lyrics(query)

    if not (resp.ok and resp.result):
        return await m.edit("No lyrics found.")

    song = resp.result[0]
    song_name = song["song"]
    artist = song["artist"]
    lyrics = song["lyrics"]
    msg = f"**{song_name}** | **{artist}**\n\n__{lyrics}__"

    if len(msg) > 4095:
        msg = await paste(msg)
        msg = f"**LYRICS_TOO_LONG:** [URL]({msg})"
    return await m.edit(msg)
