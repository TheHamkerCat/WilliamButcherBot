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
from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.utils.functions import get_http_status_code
from wbb.utils.pastebin import paste

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To Nekobin"


@app.on_message(filters.command("paste") & ~filters.edited)
@capture_err
async def paste_func(_, message):
    if message.reply_to_message:
        app.set_parse_mode("markdown")
        if message.reply_to_message.text:
            m = await message.reply_text("Pasting...")
            content = str(message.reply_to_message.text)
            link = await paste(content)
            preview = link + "/preview.png"
            status_code = await get_http_status_code(preview)
            i = 0
            while status_code != 200:
                if i == 5:
                    break
                status_code = await get_http_status_code(preview)
                await asyncio.sleep(0.2)
                i += 1
            await m.delete()
            await app.send_photo(message.chat.id, photo=preview, caption=link)

        elif message.reply_to_message.document:
            if message.reply_to_message.document.file_size > 1048576:
                await message.reply_text("You can only paste files smaller than 1MB.")
                return
            m = await message.reply_text("Pasting...")
            doc_file = await message.reply_to_message.download(file_name="paste.txt")
            i = open(doc_file, "r")
            link = await paste(i.read())
            preview = link + "/preview.png"
            status_code = await get_http_status_code(preview)
            i = 0
            while status_code != 200:
                if i == 5:
                    break
                status_code = await get_http_status_code(preview)
                await asyncio.sleep(0.2)
                i += 1
            await m.delete()
            await app.send_photo(message.chat.id, photo=preview, caption=link)
            os.remove(doc_file)
    else:
        await message.reply_text("Reply To A Message With /paste")
