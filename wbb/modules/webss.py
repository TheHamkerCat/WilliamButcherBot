from wbb import app, app2, SUDOERS
from wbb.utils.errors import capture_err
from pyrogram import filters
from pyppeteer import launch
import os
import asyncio
import time

__MODULE__ = "WebSS"
__HELP__ = "/webss | .webss [URL] - Take A Screenshot Of A Webpage"


@app.on_message(filters.command("webss") & filters.user(SUDOERS))
@app2.on_message(filters.command("webss", prefixes=["."]) & filters.user(SUDOERS))
@capture_err
async def take_ss(_, message):
    if len(message.command) != 2:
        await message.reply_text("Give A Url To Fetch Screenshot.")
        return
    start_time = time.time()
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("**Launching Browser**")
    browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
            )
    await m.edit("**Loading Page**")
    page = await browser.newPage()
    await page.setViewport({'width': 2000, 'height': 1381, 'deviceScaleFactor': 2.0})
    await page.goto(url, {'waitUntil': 'load'})
    await asyncio.sleep(1)
    await m.edit("**Taking Screenshot**")
    await page.screenshot({'path': 'webss.png'})
    await m.delete()
    end_time = time.time()
    await message.reply_photo(
            'webss.png',
            caption=f"`{url}`\n__Took {round(end_time - start_time)} Seconds.__")
    await browser.close()
    os.remove('webss.png')
