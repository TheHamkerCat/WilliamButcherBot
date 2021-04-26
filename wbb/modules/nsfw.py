from wbb import app, arq, SUDOERS, IMGBB_API_KEY
from wbb.utils.filter_groups import nsfw_detect_group
from pyrogram import filters
from random import randint
import aiohttp
import aiofiles
import os


@app.on_message(filters.document | filters.photo & ~filters.private, group=nsfw_detect_group)
async def detect_nsfw(_, message):
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
    image = await message.download(f"{randint(6666, 9999)}.jpg")
    async with aiofiles.open(image, mode='rb') as f:
        payload = {
        "key": IMGBB_API_KEY,
        "image": await f.read(),
        "expiration": "60"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.imgbb.com/1/upload", data=payload) as resp:
            data = await resp.json()
        url = data['data']['url']
    os.remove(image)
    results = await arq.nsfw_scan(url)
    hentai = results.data.hentai
    sexy = results.data.sexy
    porn = results.data.porn
    neutral = results.data.neutral
    if hentai < 80 and porn < 70 and sexy < 80:
        return
    if neutral > 30:
        return
    await message.delete()
    user_mention = message.from_user.mention
    user_id = message.from_user.id
    await message.reply_text(f"""
**NSFW Image Detected & Deleted Successfully!
————————————————————————**

**User:** {user_mention} [`{user_id}`]
**Safe:** `{neutral}`
**Porn:** `{porn}`
**Adult:** `{sexy}`
**Hentai:** `{hentai}`
""")
