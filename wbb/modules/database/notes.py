from typing import Dict, List, Union
from . import db

notes = db.notes


async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notes.find_one({"chat_id": chat_id})
    _notes = {} if not _notes else _notes["notes"]
    return _notes


async def save_note(chat_id: int, name: str, note: dict):
    name = name.lower()
    _notes = await _get_notes(chat_id)
    _notes[name] = note

    await notes.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "notes": _notes
            }
        },
        upsert=True
    )


async def get_note_names(chat_id: int) -> List[str]: return [note for note in await _get_notes(chat_id)]


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    _notes = await _get_notes(chat_id)
    return _notes[name] if name in _notes else False
