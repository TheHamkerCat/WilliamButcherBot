import os
from asyncio import get_running_loop
from random import randint

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.utils.functions import get_file_id_from_message


@app.on_message(filters.command("reverse"))
@capture_err
async def reverse_image_search(_, message):
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
    m = await message.reply_text("Downloading")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Can't reverse that")
    image = await app.download_media(
        file_id, f"{randint(1000, 10000)}.jpg"
    )
    await m.edit("Uploading to google's server")
    async with aiofiles.open(image, "rb") as f:
        if image:
            search_url = "http://www.google.com/searchbyimage/upload"
            multipart = {
                "encoded_image": (image, await f.read()),
                "image_content": "",
            }

            def post_non_blocking():
                return requests.post(
                    search_url, files=multipart, allow_redirects=False
                )

            loop = get_running_loop()
            response = await loop.run_in_executor(
                None, post_non_blocking
            )
            location = response.headers.get("Location")
            os.remove(image)
        else:
            return await m.edit("Something wrong happened.")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
    }
    await m.edit("Scraping query")
    async with aiohttp.ClientSession() as session:
        async with session.get(location, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
    div = soup.find_all("div", {"class": "r5a77d"})[0]
    anchor_element = div.find("a")
    text = anchor_element.text
    try:
        await m.edit("Trying to send a photo")
        await app.send_photo(
            message.chat.id,
            photo=f"https://webshot.amanoteam.com/print?q={location}",
            caption=f"**Result**: [{text}]({location})",
        )
        await m.delete()
    except Exception:
        text = f"**Result**: [Link]({location})"
        await m.edit(text)
