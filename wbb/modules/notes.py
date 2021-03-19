from wbb import app, db
from pyrogram import filters


notes = db.notes # Notes collection


@app.on_message(filters.command("save") & ~filters.edited & ~filters.private)
async def save_note(_, message):
    if len(message.command) < 2 or not message.reply_to_message:
        await message.reply_text("Usage:\nReply to a text or sticker with /save [NOTE_NAME] to save it.")
        return
    print("passed return 1")
    if not message.reply_to_message.text and not message.reply_to_message.sticker:
        await message.reply_text("__**You can only save text or stickers in notes.**__")
        return
    print("passed return 2")
    note_name = message.text.split(None, 1)[1]
    note_type = "text" if message.reply_to_message.text else "sticker"
    note_data = message.reply_to_message.text.markdown if note_type == "text" else message.reply_to_message.sticker.file_id
    chat_id = message.chat.id
    current_note = {
            "name": note_name,
            "type": note_type,
            "data": note_data
            }
    notes_cursor = notes.find({"chat_id": chat_id}) # Cursor object of all notes in a chat

    for notes_list in await notes_cursor.to_list(length=1):
        chat_notes = notes_list['notes']
    chat_notes.append(current_note)

    await note.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": chat_notes}},
            upsert=True
            )
    await message.reply_text(f"__**Saved note {note_name}.**__")


@app.on_message(filters.command("notes") & ~filters.edited & ~filters.private)
async def get_notes(_, message):
    chat_id = message.chat.id
    notes_cursor = notes.find({"chat_id": chat_id}) # Cursor object of all notes in a chat

    for notes_list in await notes_cursor.to_list(length=1):
        note = notes_list['notes']
    try:
        if len(note) == 0:
            await message.reply_text("__**No notes in this chat.**__")
            return
    except UnboundLocalError:
            await message.reply_text("__**No notes in this chat.**__")
            return
    msg = ""
    for note in notes:
        msg += f"`{note['name']}`\n"
    await message.reply_text(msg)


@app.on_message(filters.command("get") & ~filters.edited & ~filters.private)
async def get_note(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage**\n__/get [NOTE_NAME]__")
        return
    note_name = message.text.split(None, 1)[1]
    chat_id = message.chat.id  
    notes_cursor = notes.find({"chat_id": chat_id}) # Cursor object of all notes in a chat

    for notes_list in await notes_cursor.to_list(length=1):
        note = notes_list['notes']
    try:
        if len(note) == 0:
            await message.reply_text("__**No note with this name.**__")
            return
    except UnboundLocalError:
            await message.reply_text("__**No note with this name.**__")
            return

    for note in notes:
        if note['name'] == note_name:
            if note['type'] == "sticker":
                await message.reply_sticker(note['data'])
                return
            await message.reply_text(note['data'])
            return
    await message.reply_text("**There are no notes in this chat matching your query.**")

