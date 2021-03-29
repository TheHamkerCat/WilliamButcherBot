from pyrogram import filters
from wbb import vc, arq, app
from wbb.utils.errors import capture_err
from wbb.utils.botinfo import USERBOT_ID
import ffmpeg
import aiohttp
import aiofiles

__MODULE__ = "Voice Chat"
__HELP__ = """/joinvc - To Join A Voice Chat
/music [SONG_NAME] - To Play Music In VC"""


@app.on_message(filters.command("joinvc") & filters.user(USERBOT_ID))
@capture_err
async def joinvc(_, message):
    if vc.is_connected:
        await message.reply_text("__**Bot Is Already In Voice Chat.**__")
        return
    await vc.start(message.chat.id)
    await message.reply_text("__**Joined The Voice Chat.**__")


@app.on_message(filters.command("music") & filters.user(USERBOT_ID))
@capture_err
async def play_music(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage:**\n/music [SONG_NAME]")
        return
    m = await message.reply_text("__**Searching**__")
    query = message.text.split(None, 1)[1]
    song = (await arq.saavn(query))[0]
    await m.edit("__**Downloading**__")
    await download_and_transcode_song(song.media_url)
    await m.edit(f"__**Playing {song.song}\n**__")


async def download_and_transcode_song(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open('song.mp3', mode='wb')
                await f.write(await resp.read())
                await f.close()
    transcode("song.mp3")


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le',
                                  acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run()
    os.remove(filename)
