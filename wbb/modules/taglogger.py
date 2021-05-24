from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from wbb import (BOT_ID, LOG_GROUP_ID, LOG_MENTIONS, USERBOT_ID, USERBOT_NAME,
                 USERBOT_USERNAME, app, app2)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import taglog_group

__MODULE__ = "Tag Logger"
__HELP__ = """
THIS MODULE IS ONLY FOR SUDOERS

This module logs every action that contains your id, name, username, mention.
"""

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
**User:** {message.from_user.mention} [`{message.from_user.id if message.from_user else None}`]
**Text:** {message.text if message.text else message.caption if message.caption else None}
**Chat:** {message.chat.title} [`{message.chat.id}`]
**Bot:** {message.from_user.is_bot}
"""
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="Check Action", url=message.link))
    await app.send_message(LOG_GROUP_ID, text=msg, reply_markup=button)


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
        if reply_message.from_user:
            if reply_message.from_user.id == USERBOT_ID:
                await sendLog(message)
                return

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
        return
