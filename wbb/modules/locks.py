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
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.modules.admin import current_chat_permissions, list_admins
from wbb.utils.functions import get_urls_from_text

__MODULE__ = "Locks"
__HELP__ = """
Commands: /lock | /unlock | /locks [No Parameters Required]

Parameters:
    messages | stickers | gifs | media | games | polls

    inline  | url | group_info | user_add | pin

You can only pass the "all" parameter with /lock, not with /unlock

Example:
    /lock all
"""

incorrect_parameters = "Incorrect Parameters, Check Locks Section In Help."
# Using disable_preview as a switch for url checker
# That way we won't need an additional db to check
# If url lock is enabled/disabled for a chat
data = {
    "messages": "can_send_messages",
    "stickers": "can_send_stickers",
    "gifs": "can_send_animations",
    "media": "can_send_media_messages",
    "games": "can_send_games",
    "inline": "can_use_inline_bots",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "group_info": "can_change_info",
    "useradd": "can_invite_users",
    "pin": "can_pin_messages",
}


async def tg_lock(message, permissions: list, perm: str, lock: bool):
    if lock:
        if perm not in permissions:
            return await message.reply_text("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply_text("Already Unlocked.")
        permissions.append(perm)

    permissions = {perm: True for perm in list(set(permissions))}

    try:
        await app.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply_text(
            "To unlock this, you have to unlock 'messages' first."
        )

    await message.reply_text(("Locked." if lock else "Unlocked."))


@app.on_message(filters.command(["lock", "unlock"]) & ~filters.private)
@adminsOnly("can_restrict_members")
async def locks_func(_, message):
    if len(message.command) != 2:
        return await message.reply_text(incorrect_parameters)

    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()

    if parameter not in data and parameter != "all":
        return await message.reply_text(incorrect_parameters)

    permissions = await current_chat_permissions(chat_id)

    if parameter in data:
        await tg_lock(
            message,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        await app.set_chat_permissions(chat_id, ChatPermissions())
        await message.reply_text(f"Locked Everything in {message.chat.title}")

    elif parameter == "all" and state == "unlock":
        await app.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_stickers=True,
                can_send_animations=True,
                can_invite_users=True,
                can_send_games=True,
                can_use_inline_bots=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
            ),
        )
        await message.reply(f"Unlocked Everything in {message.chat.title}")


@app.on_message(filters.command("locks") & ~filters.private)
@capture_err
async def locktypes(_, message):
    permissions = await current_chat_permissions(message.chat.id)

    if not permissions:
        return await message.reply_text("No Permissions.")

    perms = ""
    for i in permissions:
        perms += f"__**{i}**__\n"

    await message.reply_text(perms)


@app.on_message(filters.text & ~filters.private, group=69)
async def url_detector(_, message):
    user = message.from_user
    chat_id = message.chat.id
    text = message.text.lower().strip()

    if not text or not user:
        return
    if user.id in (SUDOERS + (await list_admins(chat_id))):
        return

    check = get_urls_from_text(text)
    if check:
        permissions = await current_chat_permissions(chat_id)
        if "can_add_web_page_previews" not in permissions:
            try:
                await message.delete()
            except Exception:
                await message.reply_text(
                    "This message contains a URL, "
                    + "but i don't have enough permissions to delete it"
                )
