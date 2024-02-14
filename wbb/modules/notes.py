"""
MIT License

Copyright (c) 2023 TheHamkerCat

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

from re import findall

from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from wbb import SUDOERS, USERBOT_ID, USERBOT_PREFIX, app, app2, eor
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.keyboard import ikb
from wbb.modules.admin import member_permissions
from wbb.utils.dbfunctions import (
    delete_note,
    deleteall_notes,
    get_note,
    get_note_names,
    save_note,
)
from wbb.utils.functions import (
    check_format,
    extract_text_and_keyb,
    get_data_and_name,
)

__MODULE__ = "Notes"
__HELP__ = """/notes To Get All The Notes In The Chat.

/save [NOTE_NAME] To Save A Note.

Supported note types are Text, Animation, Photo, Document, Video, video notes, Audio, Voice.

To change caption of any files use.\n/save [NOTE_NAME] [NEW_CAPTION].

#NOTE_NAME To Get A Note.

/delete [NOTE_NAME] To Delete A Note.
/deleteall To delete all the notes in a chat (permanently).

Checkout /markdownhelp to know more about formattings and other syntax.
"""


def extract_urls(reply_markup):
    urls = []
    if reply_markup.inline_keyboard:
        buttons = reply_markup.inline_keyboard
        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                if button.url:
                    name = (
                        "\n~\nbutton"
                        if i * len(row) + j + 1 == 1
                        else f"button{i * len(row) + j + 1}"
                    )
                    urls.append((f"{name}", button.text, button.url))
    return urls


@app2.on_message(filters.command("save", prefixes=USERBOT_PREFIX) & SUDOERS & ~filters.via_bot)
@app.on_message(filters.command("save") & ~filters.private)
@adminsOnly("can_change_info")
async def save_notee(_, message):
    try:
        if len(message.command) < 2:
            await eor(
                message,
                text="**Usage:**\nReply to a message with /save [NOTE_NAME] to save a new note.",
            )
        else:
            replied_message = message.reply_to_message
            if not replied_message:
                replied_message = message
            data, name = await get_data_and_name(replied_message, message)
            if data == "error":
                return await message.reply_text(
                    "**Usage:**\n__/save [NOTE_NAME] [CONTENT]__\n`-----------OR-----------`\nReply to a message with.\n/save [NOTE_NAME]"
                )
            if replied_message.text:
                _type = "text"
                file_id = None
            if replied_message.sticker:
                _type = "sticker"
                file_id = replied_message.sticker.file_id
            if replied_message.animation:
                _type = "animation"
                file_id = replied_message.animation.file_id
            if replied_message.photo:
                _type = "photo"
                file_id = replied_message.photo.file_id
            if replied_message.document:
                _type = "document"
                file_id = replied_message.document.file_id
            if replied_message.video:
                _type = "video"
                file_id = replied_message.video.file_id
            if replied_message.video_note:
                _type = "video_note"
                file_id = replied_message.video_note.file_id
            if replied_message.audio:
                _type = "audio"
                file_id = replied_message.audio.file_id
            if replied_message.voice:
                _type = "voice"
                file_id = replied_message.voice.file_id
            if replied_message.reply_markup and not "~" in data:
                urls = extract_urls(replied_message.reply_markup)
                if urls:
                    response = "\n".join(
                        [f"{name}=[{text}, {url}]" for name, text, url in urls]
                    )
                    data = data + response
            if data:
                data = await check_format(ikb, data)
                if not data:
                    return await message.reply_text(
                        "**Wrong formatting, check the help section.**"
                    )
            note = {
                "type": _type,
                "data": data,
                "file_id": file_id,
            }
            chat_id = USERBOT_ID if message.text.startswith(USERBOT_PREFIX) else message.chat.id
            await save_note(chat_id, name, note)
            await eor(message, text=f"__**Saved note {name}.**__")
    except UnboundLocalError:
        return await message.reply_text(
            "**Replied message is inaccessible.\n`Forward the message and try again`**"
        )


@app2.on_message(
    filters.command("notes", prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & SUDOERS
)
@app.on_message(filters.command("notes") & ~filters.private)
@capture_err
async def get_notes(_, message):
    prefix = message.text.split()[0][0]
    is_ubot = bool(prefix == USERBOT_PREFIX)
    chat_id = USERBOT_ID if is_ubot else message.chat.id

    _notes = await get_note_names(chat_id)

    if not _notes:
        return await eor(message, text="**No notes in this chat.**")
    _notes.sort()
    msg = f"List of notes in {'USERBOT' if is_ubot else message.chat.title}\n"
    for note in _notes:
        msg += f"**-** `{note}`\n"
    await eor(message, text=msg)


@app2.on_message(
    filters.command("get", prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & SUDOERS
)
async def get_one_note_userbot(_, message):
    if len(message.text.split()) < 2:
        return await eor(message, text="Invalid arguments")

    name = message.text.split(None, 1)[1]

    _note = await get_note(USERBOT_ID, name)
    if not _note:
        return await eor(message, text="No such note.")

    type = _note["type"]
    data = _note["data"]
    file_id = _note.get("file_id")
    keyb = None
    await get_reply(message, type, file_id, data, keyb, protect)


@app.on_message(filters.regex(r"^#.+") & filters.text & ~filters.private)
@capture_err
async def get_one_note(_, message):
    chat_id = message.chat.id
    name = message.text.replace("#", "", 1)
    if not name:
        return
    _note = await get_note(message.chat.id, name)
    if not _note:
        return
    type = _note["type"]
    data = _note["data"]
    file_id = _note.get("file_id")
    keyb = None
    if data:
        if "{chat}" in data:
            data = data.replace("{chat}", message.chat.title)
        if "{name}" in data:
            data = data.replace(
                "{name}", message.from_user.mention
            )
        if findall(r"\[.+\,.+\]", data):
            keyboard = extract_text_and_keyb(ikb, data)
            if keyboard:
                data, keyb = keyboard
    replied_message = message.reply_to_message
    if replied_message:
        if replied_message.from_user.id != message.from_user.id:
            message = replied_message
    await get_reply(message, type, file_id, data, keyb)


async def get_reply(message, type, file_id, data, keyb):
    if type == "text":
        await message.reply_text(
            text=data,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    if type == "sticker":
        await message.reply_sticker(
            sticker=file_id,
        )
    if type == "animation":
        await message.reply_animation(
            animation=file_id,
            caption=data,
            reply_markup=keyb,
        )
    if type == "photo":
        await message.reply_photo(
            photo=file_id,
            caption=data,
            reply_markup=keyb,
        )
    if type == "document":
        await message.reply_document(
            document=file_id,
            caption=data,
            reply_markup=keyb,
        )
    if type == "video":
        await message.reply_video(
            video=file_id,
            caption=data,
            reply_markup=keyb,
        )
    if type == "video_note":
        await message.reply_video_note(
            video_note=file_id,
        )
    if type == "audio":
        await message.reply_audio(
            audio=file_id,
            caption=data,
            reply_markup=keyb,
        )
    if type == "voice":
        await message.reply_voice(
            voice=file_id,
            caption=data,
            reply_markup=keyb,
        )


@app2.on_message(
    filters.command("delete", prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & SUDOERS
)
@app.on_message(filters.command("delete") & ~filters.private)
@adminsOnly("can_change_info")
async def del_note(_, message):
    if len(message.command) < 2:
        return await eor(message, text="**Usage**\n__/delete [NOTE_NAME]__")
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await eor(message, text="**Usage**\n__/delete [NOTE_NAME]__")

    prefix = message.text.split()[0][0]
    is_ubot = bool(prefix == USERBOT_PREFIX)
    chat_id = USERBOT_ID if is_ubot else message.chat.id

    deleted = await delete_note(chat_id, name)
    if deleted:
        await eor(message, text=f"**Deleted note {name} successfully.**")
    else:
        await eor(message, text="**No such note.**")


@app.on_message(filters.command("deleteall") & ~filters.private)
@adminsOnly("can_change_info")
async def delete_all(_, message):
    _notes = await get_note_names(message.chat.id)
    if not _notes:
        return await message.reply_text("**No notes in this chat.**")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "YES, DO IT", callback_data="delete_yes"
                    ),
                    InlineKeyboardButton("Cancel", callback_data="delete_no"),
                ]
            ]
        )
        await message.reply_text(
            "**Are you sure you want to delete all the notes in this chat forever ?.**",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("delete_(.*)"))
async def delete_all_cb(_, cb):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_change_info"
    if permission not in permissions:
        return await cb.answer(
            f"You don't have the required permission.\n Permission: {permission}",
            show_alert=True,
        )
    input = cb.data.split("_", 1)[1]
    if input == "yes":
        stoped_all = await deleteall_notes(chat_id)
        if stoped_all:
            return await cb.message.edit(
                "**Successfully deleted all notes on this chat.**"
            )
    if input == "no":
        await cb.message.reply_to_message.delete()
        await cb.message.delete()
