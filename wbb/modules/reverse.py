import os
from random import randint

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from pyrogram import filters

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Reverse"
__HELP__ = "/reverse  - Reverse search an image. [SUDOERS ONLY]"


@app.on_message(filters.command("reverse"))
@capture_err
async def reverse_image_search(_, message):
    if message.from_user.id not in SUDOERS:
        return await message.reply_text("THIS FEATURE IS ONLY FOR SUDO USERS.")
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to reverse search it."
        )
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        return await message.reply_text(
            "Reply to an image/document/sticker/animation to reverse search it."
        )
    m = await message.reply_text("Searching")
    if reply.document:
        if int(reply.document.file_size) > 3145728:
            return await m.edit("File too large")
        mime_type = reply.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return await m.edit("Document Mimetype Invalid")
        file_id = reply.document.file_id
    if reply.sticker:
        if reply.sticker.is_animated:
            if not reply.sticker.thumbs:
                return await m.edit("Sticker Has No Thumb")
            file_id = reply.sticker.thumbs[0].file_id
        else:
            file_id = reply.sticker.file_id

    if reply.photo:
        file_id = reply.photo.file_id

    if reply.animation:
        if not reply.animation.thumbs:
            return await m.edit(
                "Gif Has No Thumbnail, so it cannot be reverse searched"
            )
        file_id = reply.animation.thumbs[0].file_id

    if reply.video:
        if not reply.video.thumbs:
            return
        file_id = reply.video.thumbs[0].file_id
    image = await app.download_media(file_id, f"{randint(1000, 10000)}.jpg")
    async with aiofiles.open(image, "rb") as f:
        if image:
            search_url = "http://www.google.com/searchbyimage/upload"
            multipart = {
                "encoded_image": (image, await f.read()),
                "image_content": "",
            }
            response = requests.post(
                search_url, files=multipart, allow_redirects=False
            )
            location = response.headers.get("Location")
            os.remove(image)
        else:
            return await m.edit("Something wrong happened.")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(location, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
    div = soup.find_all("div", {"class": "r5a77d"})[0]
    anchor_element = div.find("a")
    text = anchor_element.text
    try:
        await app.send_photo(
            message.chat.id,
            photo=f"https://webshot.amanoteam.com/print?q={location}",
            caption=f"**Query** [{text}]({location})",
        )
        await m.delete()
    except Exception:
        text = f"**Result**: [Link]({location})"
        await m.edit(text)
