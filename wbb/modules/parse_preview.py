"""
MIT License

Copyright (c) present TheHamkerCat

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

from pyrogram import filters, enums
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_PREFIX, app2, eor
from wbb.core.sections import section


@app2.on_message(
    filters.command("parse_preview", prefixes=USERBOT_PREFIX) 
    & SUDOERS
)
async def parse(_, message: Message):
    r = message.reply_to_message
    has_wpp = False
    if not r:
        return await eor(message, text="Reply to a message with a webpage")

    m_ = await eor(message, text="Parsing...")

    if not r.web_page:
        text = r.text or r.caption
        if text:
            m = await app2.send_message("me", text)
            await asyncio.sleep(1)
            await m.delete()
            if m.web_page:
                r = m
                has_wpp = True
    else:
        has_wpp = True

    if not has_wpp:
        return await m_.edit(
            "Replied message has no webpage preview.",
        )

    wpp = r.web_page

    body = {
        "Title": [wpp.title or "Null"],
        "Description": [
            (wpp.description[:50] + "...") if wpp.description else "Null"
        ],
        "URL": [wpp.display_url or "Null"],
        "Author": [wpp.author or "Null"],
        "Site Name": [wpp.site_name or "Null"],
        "Type": wpp.type or "Null",
    }

    text = section("Preview", body)

    t = wpp.type

    if t == enums.MessagesFilter.PHOTO:
        media = wpp.photo
        func = app2.send_photo
    elif t == enums.MessagesFilter.AUDIO:
        media = wpp.audio
        func = app2.send_audio
    elif t == enums.MessagesFilter.VIDEO:
        media = wpp.video
        func = app2.send_video
    elif t == enums.MessagesFilter.DOCUMENT:
        media = wpp.document
        func = app2.send_document
    else:
        media = None
        func = None

    if media and func:
        await m_.delete()
        return await func(
            m_.chat.id,
            media.file_id,
            caption=text,
        )

    await m_.edit(text, disable_web_page_preview=True)
