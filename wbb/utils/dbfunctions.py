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
from wbb import db
from typing import Dict, List, Union

notesdb = db.notes
filtersdb = db.filters
warnsdb = db.warns
karmadb = db.karma
chatsdb = db.chats
gbansdb = db.gban
coupledb = db.couple
captchadb = db.captcha
antiservicedb = db.antiservice
pmpermitdb = db.pmpermit
welcomedb = db.welcome_text
nsfwdb = db.nsfw


""" Notes functions """


async def get_notes_count() -> dict:
    chats = notesdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    notes_count = 0
    for chat in await chats.to_list(length=1000000000):
        notes_name = await get_note_names(chat['chat_id'])
        notes_count += len(notes_name)
        chats_count += 1
    return {
        "chats_count": chats_count,
        "notes_count": notes_count
    }


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


async def get_filters_count() -> dict:
    chats = filtersdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    filters_count = 0
    for chat in await chats.to_list(length=1000000000):
        filters_name = await get_filters_names(chat['chat_id'])
        filters_count += len(filters_name)
        chats_count += 1
    return {
        "chats_count": chats_count,
        "filters_count": filters_count
    }


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


""" Warn functions """


async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id


async def get_warns_count() -> dict:
    chats = warnsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    warns_count = 0
    for chat in await chats.to_list(length=100000000):
        for user in chat['warns']:
            warns_count += chat['warns'][user]['warns']
        chats_count += 1
    return {
        "chats_count": chats_count,
        "warns_count": warns_count
    }


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


""" Karma functions """


async def get_karmas_count() -> dict:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    karmas_count = 0
    for chat in await chats.to_list(length=1000000):
        for i in chat['karma']:
            karmas_count += chat['karma'][i]['karma']
        chats_count += 1
    return {
        "chats_count": chats_count,
        "karmas_count": karmas_count
    }


async def user_global_karma(user_id) -> int:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return 0
    total_karma = 0
    for chat in await chats.to_list(length=1000000):
        karma = await get_karma(chat['chat_id'], await int_to_alpha(user_id))
        total_karma += int(karma['karma']) if karma else 0
    return total_karma


async def get_karmas(chat_id: int) -> Dict[str, int]:
    karma = await karmadb.find_one({"chat_id": chat_id})
    if karma:
        karma = karma['karma']
    else:
        karma = {}
    return karma


async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    if name in karmas:
        return karmas[name]


async def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    karmas[name] = karma
    await karmadb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "karma": karmas
            }
        },
        upsert=True
    )


async def is_karma_on(chat_id: int) -> bool:
    chat = await karmadb.find_one({"chat_id_toggle": chat_id})
    if not chat:
        return True
    return False


async def karma_on(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if is_karma:
        return
    return await karmadb.delete_one({"chat_id_toggle": chat_id})


async def karma_off(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if not is_karma:
        return
    return await karmadb.insert_one({"chat_id_toggle": chat_id})


""" Chats log functions """


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {'$lt': 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})


""" Gban functions """


async def get_gbans_count() -> int:
    users = gbansdb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    return await gbansdb.insert_one({"user_id": user_id})


async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await gbansdb.delete_one({"user_id": user_id})


# Couple Chooser

async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "couple": lovers
            }
        },
        upsert=True
    )

# Captcha


async def is_captcha_on(chat_id: int) -> bool:
    chat = await captchadb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def captcha_on(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if is_captcha:
        return
    return await captchadb.delete_one({"chat_id": chat_id})


async def captcha_off(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if not is_captcha:
        return
    return await captchadb.insert_one({"chat_id": chat_id})

"""Anti Service System"""


async def is_antiservice_on(chat_id: int) -> bool:
    chat = await antiservicedb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def antiservice_on(chat_id: int):
    is_antiservice = await is_antiservice_on(chat_id)
    if is_antiservice:
        return
    return await antiservicedb.delete_one({"chat_id": chat_id})


async def antiservice_off(chat_id: int):
    is_antiservice = await is_antiservice_on(chat_id)
    if not is_antiservice:
        return
    return await antiservicedb.insert_one({"chat_id": chat_id})


""" PM PERMIT """


async def is_pmpermit_approved(user_id: int) -> bool:
    user = await pmpermitdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def approve_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if is_pmpermit:
        return
    return await pmpermitdb.insert_one({"user_id": user_id})


async def disapprove_pmpermit(user_id: int):
    is_pmpermit = await is_pmpermit_approved(user_id)
    if not is_pmpermit:
        return
    return await pmpermitdb.delete_one({"user_id": user_id})


""" WELCOME FUNCTIONS """


async def get_welcome(chat_id: int) -> str:
    text = await welcomedb.find_one({"chat_id": chat_id})
    return text['text']


async def set_welcome(chat_id: int, text: str):
    return await welcomedb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "text": text
            }
        },
        upsert=True
    )


async def del_welcome(chat_id: int):
    return await welcomedb.delete_one({"chat_id": chat_id})


"""NSFW System"""


async def is_nsfw_on(chat_id: int) -> bool:
    chat = await nsfwdb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def nsfw_on(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if is_nsfw:
        return
    return await nsfwdb.delete_one({"chat_id": chat_id})


async def nsfw_off(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if not is_nsfw:
        return
    return await nsfwdb.insert_one({"chat_id": chat_id})
