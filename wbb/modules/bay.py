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
import os
import requests
import aiohttp
import aiofiles
from wbb import app, SUDOERS
from pyrogram import filters
from random import randint
from wbb.core.decorators.errors import capture_err


__MODULE__ = "BAYFILES"
__HELP__ = """/url [URL] To upload a url to bayfiles. [SUDO ONLY]
/tg To Upload a telegram file to bayfiles. [SUDO ONLY]"""


@app.on_message(filters.command("url") & filters.user(SUDOERS))
@capture_err
async def url(_, message):
    if len(message.command) != 2:
        await message.reply_text("/url [url]")
        return
    m = await message.reply_text("Downloading")
    lenk = message.text.split(None, 1)[1]
    try:
        filename = await download(lenk)
        files = {'file': open(filename, 'rb')}
        await m.edit("Uploading....")
        r = requests.post("https://api.bayfiles.com/upload", files=files)
        text = r.json()
        output = f"""
**status:** `{text['status']}`
**link:** {text['data']['file']['url']['full']}
**id:** `{text['data']['file']['metadata']['id']}`
**name:** `{text['data']['file']['metadata']['name']}`
**size:** `{text['data']['file']['metadata']['size']['readable']}`"""
        await m.edit(output)
        os.remove(filename)
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return


@app.on_message(filters.command("tg") & filters.user(SUDOERS))
@capture_err
async def tg(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    if not message.reply_to_message.media:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    m = await message.reply_text("Downloading Document.")
    fn = await message.reply_to_message.download()
    try:
        files = {'file': open(fn, 'rb')}
        await m.edit("Uploading....")
        r = requests.post("https://api.bayfiles.com/upload", files=files)
        text = r.json()
        output = f"""
**Status:** `{text['status']}`
**Link:** {text['data']['file']['url']['full']}
**ID:** `{text['data']['file']['metadata']['id']}`
**Name:** `{text['data']['file']['metadata']['name']}`
**Size:** `{text['data']['file']['metadata']['size']['readable']}`"""
        await m.edit(output)
        os.remove(fn)
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return


async def download(url):
    ext = url.split(".")[-1]
    filename = str(randint(1000, 9999)) + "." + ext
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return filename
