from wbb import db

notesdb = db.notes
filtersdb = db.filters
warnsdb = db.warns


""" Notes functions """

async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notesdb.find_one({"chat_id": chat_id})
    _notes = {} if not _notes else _notes["notes"]
    return _notes


async def save_note(chat_id: int, name: str, note: dict):
    name = name.lower()
    name = name.strip()
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


async def get_note_names(chat_id: int) -> List[str]: return [note for note in await _get_notes(chat_id)]


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower()
    name = name.strip()
    _notes = await _get_notes(chat_id)
    return _notes[name] if name in _notes else False


async def delete_note(chat_id: int, name:str) -> bool:
    notesd = await _get_notes(chat_id)
    name = name.lower()
    name = name.strip()
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
    _filters = await filtesdb.find_one({"chat_id": chat_id})
    _filters = {} if not _filters else _filters["filters"]
    return _filters


async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower()
    name = name.strip()
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


async def get_filters_names(
    chat_id: int) -> List[str]: return [_filter for _filter in await _get_filters(chat_id)]


async def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower()
    name = name.strip()
    _filters = await _get_filters(chat_id)
    return _filters[name] if name in _filters else False


async def delete_filter(chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(chat_id)
    name = name.lower()
    name = name.strip()
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


""" Warn functions """


