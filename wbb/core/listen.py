"""
MIT License

Copyright (c) 2024 TheHamkerCat

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
import asyncio
from dataclasses import dataclass

from pyrogram import Client
from pyrogram.filters import Filter
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

# Lower groups run first, so a waiting call sees each message before the bot modules do
LISTENER_GROUP = -1000


@dataclass
class _Waiter:
    chat: int | str
    filter_check: MessageHandler
    future: asyncio.Future


_waiters: dict[Client, list[_Waiter]] = {}


def _is_same_chat(message: Message, chat: int | str) -> bool:
    if isinstance(chat, int):
        return message.chat.id == chat
    username = (message.chat.username or "").lower()
    return username == chat.removeprefix("@").lower()


async def _resolve_waiters(client: Client, message: Message):
    # One message completes only the oldest matching waiter
    for waiter in list(_waiters.get(client, [])):
        if waiter.future.done() or not _is_same_chat(message, waiter.chat):
            continue
        if not await waiter.filter_check.check(client, message):
            continue
        waiter.future.set_result(message)
        return


def setup_listener(client: Client):
    """Register the handler that completes listen() calls. Call after client.start()."""
    client.add_handler(MessageHandler(_resolve_waiters), group=LISTENER_GROUP)


async def listen(
    client: Client,
    chat: int | str,
    filters: Filter | None = None,
    timeout: float | None = None,
) -> Message:
    """Wait for the next message in chat (an ID or a username) that passes filters."""
    waiter = _Waiter(
        chat=chat,
        filter_check=MessageHandler(_resolve_waiters, filters),
        future=asyncio.get_running_loop().create_future(),
    )
    client_waiters = _waiters.setdefault(client, [])
    client_waiters.append(waiter)
    try:
        return await asyncio.wait_for(waiter.future, timeout)
    finally:
        client_waiters.remove(waiter)
