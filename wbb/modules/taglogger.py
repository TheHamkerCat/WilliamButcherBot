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
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from wbb import (BOT_ID, LOG_GROUP_ID, LOG_MENTIONS, USERBOT_ID, USERBOT_NAME,
                 USERBOT_USERNAME, app, app2)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import taglog_group

IS_USERBOT_ONLINE = False


@app2.on_user_status()
async def statusUpdaterFunc(_, update):
    if update.id != USERBOT_ID:
        return
    global IS_USERBOT_ONLINE
    if update.status == "online":
        IS_USERBOT_ONLINE = True
        return
    IS_USERBOT_ONLINE = False


async def sendLog(message: Message):
    msg = f"""
**User:** {message.from_user.mention if message.from_user else None} [`{message.from_user.id if message.from_user else None}`]
**Text:** {message.text.markdown if message.text else message.caption if message.caption else None}
**Chat:** {message.chat.title} [`{message.chat.id}`]
**Bot:** {message.from_user.is_bot}
"""
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="Check Action", url=message.link))
    await app.send_message(
        LOG_GROUP_ID,
        text=msg,
        reply_markup=button,
        disable_web_page_preview=True,
    )


@app2.on_message(
    ~filters.me
    & ~filters.chat([LOG_GROUP_ID, BOT_ID])
    & ~filters.private
    & ~filters.edited,
    group=taglog_group,
)
@capture_err
async def tagLoggerFunc(_, message: Message):
    if not LOG_MENTIONS:
        return
    if IS_USERBOT_ONLINE:
        return
    if message.reply_to_message:
        reply_message = message.reply_to_message
        if reply_message.from_user and (
            reply_message.from_user.id == USERBOT_ID
        ):
            return await sendLog(message)

    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        return
    if (
        str(USERBOT_ID) in text
        or str(USERBOT_USERNAME) in text
        or USERBOT_NAME in text
    ):
        await sendLog(message)
