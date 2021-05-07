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
from wbb import app, arq
from wbb.core.decorators.errors import capture_err
from wbb.utils.functions import transfer_sh
from pyrogram import filters
from random import randint
import os

@app.on_message(filters.command("ocr"))
@capture_err
async def image_ocr(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to an image or document to perform OCR on it.")
        return
    reply = message.reply_to_message
    if not reply.document and not reply.photo and not reply.sticker and not reply.animation and not reply.video:
        await message.reply_text("Reply to an image/document/sticker/animation to perform OCR on it.")
        return
    m = await message.reply_text("Scanning")
    if reply.document:
        if int(reply.document.file_size) > 3145728:
            await m.edit("File too large")
            return
        mime_type = reply.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            await m.edit("Document Mimetype Invalid")
            return
        file_id = reply.document.file_id
    if reply.sticker:
        if reply.sticker.is_animated:
            if not reply.sticker.thumbs:
                await m.edit("Sticker Has No Thumb")
                return
            file_id = reply.sticker.thumbs[0].file_id
        else:
            file_id = reply.sticker.file_id

    if reply.photo:
        file_id = reply.photo.file_id

    if reply.animation:
        if not reply.animation.thumbs:
            await m.edit("Gif Has No Thumbnail, so it cannot be scanned for OCR")
            return
        file_id = reply.animation.thumbs[0].file_id

    if reply.video:
        if not reply.video.thumbs:
            return
        file_id = reply.video.thumbs[0].file_id

    filename = f"{randint(1000, 10000)}.jpg"
    file = await app.download_media(file_id)
    url = await transfer_sh(file)
    os.remove(file)
    data = await arq.ocr(url)
    await m.edit(data.ocr)
