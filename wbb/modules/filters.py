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
from wbb import app
from wbb.modules.admin import member_permissions
from wbb.utils.dbfunctions import (
    save_filter, get_filters_names, get_filter,
    delete_filter, is_served_chat, add_served_chat
)
from pyrogram import filters
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chat_filters_group
import re


__MODULE__ = "Filters"
__HELP__ = """/filters To Get All The Filters In The Chat.
/filter [FILTER_NAME] To Save A Filter (Can be a sticker or text).
/stop [FILTER_NAME] To Stop A Filter."""


@app.on_message(filters.command("filter") & ~filters.edited & ~filters.private)
@capture_err
async def save_filters(_, message):
    if len(message.command) < 2 or not message.reply_to_message:
        await message.reply_text("Usage:\nReply to a text or sticker with /filter [FILTER_NAME] to save it.")

    elif not message.reply_to_message.text and not message.reply_to_message.sticker:
        await message.reply_text("__**You can only save text or stickers in filters.**__")

    elif len(await member_permissions(message.chat.id, message.from_user.id)) < 1:
        await message.reply_text("**You don't have enough permissions**")
    else:
        name = message.text.split(None, 1)[1].strip()
        if not name:
            await message.reply_text("**Usage**\n__/filter [FILTER_NAME]__")
            return
        _type = "text" if message.reply_to_message.text else "sticker"
        _filter = {
            "type": _type,
            "data": message.reply_to_message.text.markdown if _type == "text" else message.reply_to_message.sticker.file_id
        }
        await save_filter(message.chat.id, name, _filter)
        await message.reply_text(f"__**Saved filter {name}.**__")


@app.on_message(filters.command("filters") & ~filters.edited & ~filters.private)
@capture_err
async def get_filterss(_, message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        await message.reply_text("**No filters in this chat.**")
    else:
        msg = f"List of filters in {message.chat.title}\n"
        for _filter in _filters:
            msg += f"**-** `{_filter}`\n"
        await message.reply_text(msg)


@app.on_message(filters.command("stop") & ~filters.edited & ~filters.private)
@capture_err
async def del_filter(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage**\n__/stop [FILTER_NAME]__")

    elif len(await member_permissions(message.chat.id, message.from_user.id)) < 1:
        await message.reply_text("**You don't have enough permissions**")

    else:
        name = message.text.split(None, 1)[1].strip()
        if not name:
            await message.reply_text("**Usage**\n__/stop [FILTER_NAME]__")
            return
        chat_id = message.chat.id
        deleted = await delete_filter(chat_id, name)
        if deleted:
            await message.reply_text(f"**Deleted filter {name}.**")
        else:
            await message.reply_text("**No such filter.**")


@app.on_message(filters.text & ~filters.edited &
                ~filters.private & ~filters.via_bot &
                ~filters.forwarded, group=chat_filters_group)
async def filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    try:
        list_of_filters = await get_filters_names(chat_id)
        for word in list_of_filters:
            pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                _filter = await get_filter(chat_id, word)
                data_type = _filter['type']
                data = _filter['data']
                if data_type == "text":
                    await message.reply_text(data, disable_web_page_preview=True)
                else:
                    await message.reply_sticker(data)
    except Exception:
        pass

    """ CHAT WATCHER """
    served_chat = await is_served_chat(chat_id)
    if served_chat:
        return
    await add_served_chat(chat_id)
    return
