from wbb import app
from wbb.utils.dbfunctions import (
        _get_notes, save_note,
        get_note_names, get_note,
        delete_note
        )
from wbb.utils.errors import capture_err
from wbb.modules.admin import member_permissions
from pyrogram import filters


__MODULE__ = "Notes"
__HELP__ = """/notes To Get All The Notes In The Chat.
/save [NOTE_NAME] To Save A Note (Can be a sticker or text).
/get [NOTE_NAME] To Get A Note.
/delete [NOTE_NAME] To Delete A Note."""


@app.on_message(filters.command("save") & ~filters.edited & ~filters.private)
@capture_err
async def save_notee(_, message):
    if len(message.command) < 2 or not message.reply_to_message:
        await message.reply_text("Usage:\nReply to a text or sticker with /save [NOTE_NAME] to save it.")
    
    elif not message.reply_to_message.text and not message.reply_to_message.sticker:
        await message.reply_text("__**You can only save text or stickers in notes.**__")
    
    elif len(await member_permissions(message.chat.id, message.from_user.id)) < 1:
        await message.reply_text("**You don't have enough permissions**")
    else:
        name = message.text.split(None, 1)[1].strip()
        if not name:
            await message.reply_text("**Usage**\n__/save [NOTE_NAME]__")
            return
        _type = "text" if message.reply_to_message.text else "sticker"
        note = {
            "type": _type,
            "data": message.reply_to_message.text.markdown if _type == "text" else message.reply_to_message.sticker.file_id
        }
        await save_note(message.chat.id, name, note)
        await message.reply_text(f"__**Saved note {name}.**__")


@app.on_message(filters.command("notes") & ~filters.edited & ~filters.private)
@capture_err
async def get_notes(_, message):
    _notes = await get_note_names(message.chat.id)

    if not _notes:
        await message.reply_text("**No notes in this chat.**")
    else:
        msg = f"List of notes in {message.chat.title}\n"
        for note in _notes:
            msg += f"**-** `{note}`\n"
        await message.reply_text(msg)


@app.on_message(filters.command("get") & ~filters.edited & ~filters.private)
@capture_err
async def get_one_note(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage**\n__/get [NOTE_NAME]__")
    else:
        name = message.text.split(None, 1)[1].strip()
        if not name:
            await message.reply_text("**Usage**\n__/get [NOTE_NAME]__")
            return
        _note = await get_note(message.chat.id, name)
        if not _note:
            await message.reply_text(f"**No such note.**")
        else:
            if _note["type"] == "text":
                await message.reply_text(_note["data"])
            else:
                await message.reply_sticker(_note["data"])


@app.on_message(filters.command("delete") & ~filters.edited & ~filters.private)
@capture_err
async def del_note(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage**\n__/delete [NOTE_NAME]__")
    
    elif len(await member_permissions(message.chat.id, message.from_user.id)) < 1:
        await message.reply_text("**You don't have enough permissions**")
    
    else:
        name = message.text.split(None, 1)[1].strip()
        if not name:
            await message.reply_text("**Usage**\n__/delete [NOTE_NAME]__")
            return
        chat_id = message.chat.id
        deleted = await delete_note(chat_id, name)
        if deleted:
            await message.reply_text(f"**Deleted note {name} successfully.**")
        else:
            await message.reply_text(f"**No such note.**")
