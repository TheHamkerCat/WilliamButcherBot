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
from time import time

from pyrogram import filters
from pyrogram.types import (CallbackQuery, ChatPermissions,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            Message)

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.modules.admin import list_admins, member_permissions
from wbb.utils.filter_groups import flood_group

__MODULE__ = "Flood"
__HELP__ = """
Anti-Flood system, the one who sends more than 7 messages in a row, gets muted for an hour (Except for admins).

And no, you can't change the number of messages or action type.
"""


DB = {}  # NOTE Use mongodb instead of a fucking dict.


def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0


@app.on_message(
    ~filters.service
    & ~filters.me
    & ~filters.private
    & ~filters.channel
    & ~filters.bot
    & ~filters.edited,
    group=flood_group,
)
@capture_err
async def flood_control_func(_, message: Message):
    chat_id = message.chat.id

    # Initialize db if not already.
    if chat_id not in DB:
        DB[chat_id] = {}

    if not message.from_user:
        reset_flood(chat_id)
        return

    user_id = message.from_user.id
    mention = message.from_user.mention

    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    # Reset floodb of current chat if some other user sends a message
    reset_flood(chat_id, user_id)

    # Ignore devs and admins
    mods = (await list_admins(chat_id)) + SUDOERS
    if user_id in mods:
        return

    # Mute if user sends more than 7 messages in a row
    if DB[chat_id][user_id] >= 7:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=int(time() + 3600),
            )
        except Exception:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🚨   Unmute   🚨",
                        callback_data=f"unmute_{user_id}",
                    )
                ]
            ]
        )
        return await message.reply_text(
            f"Imagine flooding the chat in front of me, Muted {mention} for an hour!",
            reply_markup=keyboard,
        )
    DB[chat_id][user_id] += 1


@app.on_callback_query(filters.regex("unmute_"))
async def flood_callback_func(_, cq: CallbackQuery):
    from_user = cq.from_user
    permissions = await member_permissions(cq.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    await cq.message.chat.unban_member(user_id)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__User unmuted by {from_user.mention}__"
    await cq.message.edit(text)
