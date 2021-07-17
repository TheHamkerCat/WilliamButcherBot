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
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.keyboard import revert_button, build_button
from wbb.utils.msg_types import get_msg_file
from wbb.utils.dbfunctions import (delete_note, get_note,
                                   get_note_names, save_note)

__MODULE__ = "Notes"
__HELP__ = """/notes - To Get All The Notes In The Chat.
/save [NOTE_NAME] - To Save A Note (Can be a sticker or text).
#NOTE_NAME - To Get A Note.
/delete [NOTE_NAME] - To Delete A Note.


For Buttons:
    #NOTE_NAME noformat or raw - To Get A Note Without Any Formatting

    Button Syntax:
    [Button, URL]
    EG: [This is a button, example.com]
    If you want multiple buttons on the same line, use (, 2) as such:
    [one, example.com]
    [two, google.com, 2]
    This will create two buttons on a single line, instead of one button per line.

    Keep in mind that your message MUST contain some text other than just a button!
"""


SEND = {
    "text": app.send_message,
    "button_text": app.send_message,
    "sticker": app.send_sticker,
    "animation": app.send_animation,
    "photo": app.send_photo,
    "document": app.send_document,
    "video": app.send_video,
    "audio": app.send_audio,
    "video_note": app.send_video_note,
    "voice": app.send_voice,
}


@app.on_message(
    filters.command("save") & ~filters.edited & ~filters.private
)
@adminsOnly("can_change_info")
async def save_notee(_, message):
    name = message.command
    if len(name) < 2 and message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n/save [NOTE_NAME] to save it."
        )
    if len(name) < 3 and not message.reply_to_message:
        return await message.reply_text("wut?")
    text, _type, file_id, buttons = await get_msg_file(message)
    note = {
        "text": text,
        "type": _type,
        "data": file_id,
        "button": buttons
    }
    await save_note(message.chat.id, name[1], note)
    await message.reply_text(f"__**Saved note {name[1]}.**__")


@app.on_message(
    filters.command("notes") & ~filters.edited & ~filters.private
)
@capture_err
async def get_notes(_, message):
    _notes = await get_note_names(message.chat.id)
    if not _notes:
        await message.reply_text("**No notes in this chat.**")
    else:
        msg = f"List of notes in {message.chat.title}\n"
        _notes.sort()
        for note in _notes:
            msg += f"**-** `{note}`\n"
        await message.reply_text(msg)


@app.on_message(
    filters.regex(r"^#.+")
    & filters.text
    & ~filters.edited
    & ~filters.private
)
@capture_err
async def get_one_note(_, message):
    txt = message.text.replace("#", "", 1)
    args = txt.split()
    if len(args) >= 2 and args[1].lower() in ("noformat", "raw"):
        await get_note_func(message, args[0], noformat=True)
    else:
        await get_note_func(message, args[0])


@app.on_message(
    filters.command("delete") & ~filters.edited & ~filters.private
)
@adminsOnly("can_change_info")
async def del_note(_, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage**\n__/delete [NOTE_NAME]__"
        )
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(
            "**Usage**\n__/delete [NOTE_NAME]__"
        )
    chat_id = message.chat.id
    deleted = await delete_note(chat_id, name)
    if deleted:
        await message.reply_text(
            f"**Deleted note {name} successfully.**"
        )
    else:
        await message.reply_text("**No such note.**")


async def get_note_func(message, name, noformat=False):
    reply_to = message.message_id
    if _note := await get_note(message.chat.id, name):
        _type = _note['type']
        _text = _note['text']
        _data = _note['data']
        _button = _note['button']
        if noformat:
            keyboard = None
            btn_text = revert_button(_button)
        else:
            keyboard = build_button(_button)
            btn_text = ""
        if _type in ("text", "button_text"):
            try:
                await SEND[_type](
                    message.chat.id,
                    _text + btn_text,
                    disable_web_page_preview=True,
                    reply_to_message_id=reply_to,
                    reply_markup=keyboard,
                    parse_mode="md",
                )
            except Exception:
                await message.reply_text(
                f"Button format is wrong:\n\n{_text + revert_button(_button)}"
                )
        elif _type == 'sticker':
            await SEND[_type](
                message.chat.id,
                _data,
                reply_to_message_id=reply_to,
            )
        else:
            await SEND[_type](
                message.chat.id,
                _data,
                caption=_text + btn_text,
                reply_to_message_id=reply_to,
                reply_markup=keyboard,
                parse_mode="md",
            )
