import urllib.request
import json
import asyncio
from random import randint
from pyrogram import filters
from wbb import app, arq
from wbb.utils.errors import capture_err

__MODULE__ = "Images"
__HELP__ = '''/cat  - Get Cute Cats Images
For more images like wallpapers, use inline mode.
send /inline for inline help.'''


async def delete_message_with_delay(delay, message):
    await asyncio.sleep(delay)
    await message.delete()


@app.on_message(filters.command("cat") & ~filters.edited)
@capture_err
async def cat(_, message):
    with urllib.request.urlopen(
            "https://api.thecatapi.com/v1/images/search"
    ) as url:
        data = json.loads(url.read().decode())
    cat_url = (data[0]['url'])
    await message.reply_photo(cat_url)
