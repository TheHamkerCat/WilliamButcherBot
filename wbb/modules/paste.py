"""
MIT License

Copyright (c) 2021 TheHamkerCat

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
import asyncio
import os

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import WebpageCurlFailed

from wbb import aiohttpsession, app
from wbb.core.decorators.errors import capture_err
from wbb.utils.functions import get_http_status_code
from wbb.utils.pastebin import paste

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To Nekobin"


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        elif status == 200 and size > 0:
            return True
    return False


@app.on_message(filters.command("paste") & ~filters.edited)
@capture_err
async def paste_func(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            m = await message.reply_text("Pasting...")
            content = str(message.reply_to_message.text)
            link = await paste(content)
            preview = link + "/preview.png"
            if await isPreviewUp(preview):
                await message.reply_photo(
                    photo=preview, caption=link, quote=false
                )
                return
            await m.edit(link)

        elif message.reply_to_message.document:
            if message.reply_to_message.document.file_size > 1048576:
                await message.reply_text(
                    "You can only paste files smaller than 1MB."
                )
                return
            m = await message.reply_text("Pasting...")
            doc_file = await message.reply_to_message.download(
                file_name="paste.txt"
            )
            i = open(doc_file, "r")
            link = await paste(i.read())
            preview = link + "/preview.png"
            if await isPreviewUp(preview):
                await message.reply_photo(
                    photo=preview, caption=link, quote=false
                )
                return
            await m.edit(link)
            os.remove(doc_file)
    else:
        await message.reply_text("Reply To A Message With /paste")
