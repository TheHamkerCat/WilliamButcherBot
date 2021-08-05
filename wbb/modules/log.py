from datetime import datetime

import aiofiles
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from wbb import SUDOERS, app, log_file
from wbb.core.keyboard import ikb
from wbb.utils.pastebin import paste

callback = "log_paste"


@app.on_message(filters.command("logs") & filters.user(SUDOERS))
async def logs_chat(_, message):
    keyboard = ikb({"📎   Pastebin   📎": callback})
    time = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    caption = f"""
**Time:** `{time}`
**Log Type:** `ERROR`
"""
    try:
        await message.reply_document(
            log_file, caption=caption, reply_markup=keyboard
        )
    except ValueError:
        await message.reply_text("**LOGS ARE EMPTY**")


@app.on_callback_query(filters.regex(callback))
async def paste_log_neko(_, cq: CallbackQuery):
    if cq.from_user.id not in SUDOERS:
        return await cq.answer(
            "Stop clicking at whichever thing you come across."
        )
    async with aiofiles.open(log_file, mode="r") as f:
        link = await paste(await f.read())
    message: Message = cq.message
    return await message.edit_caption(
        f"{message.caption.markdown}\n**Paste:** {link}"
    )
