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
from pyrogram import filters as filters_
from pyrogram.types import Message

from wbb import SUDOERS
from wbb import USERBOT_ID as OWNER_ID
from wbb.utils.functions import get_urls_from_text


def url(_, __, message: Message) -> bool:
    # Can't use entities to check for url because
    # monospace removes url entity

    # TODO Fix detection of those urls which
    # doesn't have schema, ex-facebook.com

    text = message.text or message.caption
    if not text:
        return False
    return bool(get_urls_from_text(text))


async def admin(_, __, message: Message) -> bool:
    if message.chat.type not in ["group", "supergroup"]:
        return False
    if not message.from_user:
        if not message.sender_chat:
            return False
        return True
    # Calling iter_chat_members again and again
    # doesn't cause floodwait, that's why i'm using it here.
    return message.from_user.id in [
        member.user.id
        async for member in message._client.iter_chat_members(
            message.chat.id, filter="administrators"
        )
    ]


def entities(_, __, message: Message) -> bool:
    return bool(message.entities)


def anonymous(_, __, message: Message) -> bool:
    return bool(message.sender_chat)


def sudoers(_, __, message: Message) -> bool:
    if not message.from_user:
        return False
    return message.from_user.id in SUDOERS


def owner(_, __, message: Message) -> bool:
    if not message.from_user:
        return False
    return message.from_user.id == OWNER_ID


class Filters:
    pass


filters = Filters
filters.url = filters_.create(url)
filters.admin = filters_.create(admin)
filters.entities = filters_.create(entities)
filters.anonymous = filters_.create(anonymous)
filters.sudoers = filters_.create(sudoers)
filters.owner = filters_.create(owner)
