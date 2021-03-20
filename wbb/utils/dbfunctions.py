from wbb import db
from typing import Dict, List, Union


notesdb = db.notes
filtersdb = db.filters
warnsdb = db.warns


""" Notes functions """


async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notesdb.find_one({"chat_id": chat_id})
    if _notes:
        _notes = _notes["notes"]
    else:
        _notes = {}
    return _notes


async def get_note_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_notes(chat_id):
        _notes.append(note)
    return _notes


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_note(chat_id: int, name: str, note: dict):
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    _notes[name] = note

    await notesdb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "notes": _notes
            }
        },
        upsert=True
    )


async def delete_note(chat_id: int, name: str) -> bool:
    notesd = await _get_notes(chat_id)
    name = name.lower().strip()
    if name in notesd:
        del notesd[name]
        await notesdb.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "notes": notesd
                }
            },
            upsert=True
        )
        return True
    return False


""" Filters funcions """


async def _get_filters(chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"chat_id": chat_id})
    if _filters:
        _filters = _filters['filters']
    else:
        _filters = {}
    return _filters


async def get_filters_names(chat_id: int) -> List[str]:
    _filters = []
    for _filter in await _get_filters(chat_id):
        _filters.append(_filter)
    return _filters


async def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    if name in _filters:
        return _filters[name]
    else:
        return False


async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    _filters[name] = _filter

    await filtersdb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "filters": _filters
            }
        },
        upsert=True
    )


async def delete_filter(chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        await filtersdb.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "filters": filtersd
                }
            },
            upsert=True
        )
        return True
    return False


""" Warn function """
async def int_to_alpha(user_id):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if warns:
        warns = warns['warns']
    else:
        warns = {}
    return warns


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "warns": warns
            }
        },
        upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "warns": warnsd
                }
            },
            upsert=True
        )
        return True
    return False


