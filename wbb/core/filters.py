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
from pyrogram.filters import create
from pyrogram.types import Message
from wbb import SUDOERS, USERBOT_ID
from wbb.utils.functions import get_urls_from_text


def url(_, __, message: Message) -> bool:
    # Can't use entities to check for url because
    # monospace removes url entity

    # TODO Fix detection of those urls which
    # doesn't have schema, ex-facebook.com

    text = message.text or message.caption
    return bool(get_urls_from_text(text)) if text else False


def entities(_, __, message: Message) -> bool:
    return bool(message.entities)


def anonymous(_, __, message: Message) -> bool:
    return bool(message.sender_chat)


def sudoers(_, __, message: Message) -> bool:
    return message.from_user.id in SUDOERS if message.from_user else False


def owner(_, __, message: Message) -> bool:
    return message.from_user.id == USERBOT_ID if message.from_user else False


def edited_filter(_, __, m: Message):
    return bool(m.edit_date)


class Filters:
    pass


Customfilters = Filters
Customfilters.url = create(url)
Customfilters.entities = create(entities)
Customfilters.anonymous = create(anonymous)
Customfilters.sudoers = create(sudoers)
Customfilters.owner = create(owner)
Customfilters.edited = create(edited_filter)
