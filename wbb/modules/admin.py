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
import asyncio

from pyrogram import filters
from pyrogram.types import (CallbackQuery, ChatPermissions,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            Message)

from wbb import BOT_ID, SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import (add_warn, get_warn, int_to_alpha,
                                   remove_warns)

__MODULE__ = "Admin"
__HELP__ = """/ban - Ban A User
/unban - Unban A User
/warn - Warn A User
/rmwarn - Remove 1 Warning Of A User
/rmwarns - Remove All Warning of A User
/warns - Show Warning Of A User
/kick - Kick A User
/purge - Purge Messages
/del - Delete Replied Message
/promote - Promote A Member
/demote - Demote A Member
/pin - Pin A Message
/mute - Mute A User
/unmute - Unmute A User
/ban_ghosts - Ban Deleted Accounts
/report | @admins - Report A Message To Admins."""


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = await app.get_chat_member(chat_id, user_id)
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from wbb.core.decorators.permissions import adminsOnly


async def list_admins(chat_id: int):
    return [
        member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_stickers:
        perms.append("can_send_stickers")
    if perm.can_send_animations:
        perms.append("can_send_animations")
    if perm.can_send_games:
        perms.append("can_send_games")
    if perm.can_use_inline_bots:
        perms.append("can_use_inline_bots")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


# Get List Of Members In A Chat


async def list_members(group_id):
    list_of_members = []
    async for member in app.iter_chat_members(group_id):
        list_of_members.append(member.user.id)
    return list_of_members


# Purge Messages


@app.on_message(filters.command("purge") & ~filters.edited)
@adminsOnly("can_delete_messages")
async def purgeFunc(client, message: Message):
    chat_id = message.chat.id
    message_ids = []
    if message.chat.type not in ("supergroup", "channel"):
        return
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To A Message To Delete From, Don't Make Fun Of Yourself!"
        )
    await message.delete()
    for a_s_message_id in range(
        message.reply_to_message.message_id, message.message_id
    ):
        message_ids.append(a_s_message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id, message_ids=message_ids, revoke=True
        )


# Kick members


@app.on_message(filters.command("kick") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    if len(message.command) == 2:
        user_id = (await app.get_users(message.text.split(None, 1)[1])).id
    elif len(message.command) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to kick."
        )
    if user_id in SUDOERS:
        await message.reply_text("You Wanna Kick The Elevated One?")
    else:
        await message.chat.kick_member(user_id)
        await asyncio.sleep(1)
        await message.reply_text("Kicked!")
        await message.chat.unban_member(user_id)


# Ban members


@app.on_message(filters.command("ban") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    if len(message.command) == 2:
        user_id = (await app.get_users(message.text.split(None, 1)[1])).id
    elif len(message.command) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to ban."
        )
    if user_id in SUDOERS:
        await message.reply_text("You Wanna Ban The Elevated One?")
    else:
        await message.chat.kick_member(user_id)
        await message.reply_text("Banned!")


# Unban members


@app.on_message(filters.command("unban") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def unbanFunc(_, message: Message):
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    await message.reply_text("Unbanned!")


# Delete messages


@app.on_message(filters.command("del") & ~filters.edited)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Delete It")
    await message.reply_to_message.delete()
    await message.delete()


# Promote Members


@app.on_message(filters.command("promote") & ~filters.edited)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    chat_id = message.chat.id
    bot = await app.get_chat_member(chat_id, BOT_ID)
    if len(message.command) == 2:
        username = message.text.split(None, 1)[1]
        user_id = (await app.get_users(username)).id
    elif len(message.command) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Reply To A User's Message Or Give A Username To Promote."
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=bot.can_change_info,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=bot.can_pin_messages,
        can_promote_members=bot.can_promote_members,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    await message.reply_text("Promoted!")


# Demote Member


@app.on_message(filters.command("demote") & ~filters.edited)
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    if len(message.command) == 2:
        username = message.text.split(None, 1)[1]
        user_id = (await app.get_users(username)).id
    elif len(message.command) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Reply To A User's Message Or Give A Username To Demote."
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    await message.reply_text("Demoted!")


# Pin Messages


@app.on_message(filters.command("pin") & ~filters.edited)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Pin.")
    await message.reply_to_message.pin(disable_notification=True)


# Mute members


@app.on_message(filters.command("mute") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    if len(message.command) == 2:
        user = await app.get_users(message.text.split(None, 1)[1])
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to mute."
        )
    if user.id in SUDOERS:
        return await message.reply_text("You Wanna Mute The Elevated One?")
    await message.chat.restrict_member(user.id, permissions=ChatPermissions())
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🚨   Unmute   🚨", callback_data=f"unmute_{user.id}"
                )
            ]
        ]
    )
    await message.reply_text(
        f"Enough freedom of speech, Muted {user.mention} !",
        reply_markup=keyboard,
    )


# Unmute members


@app.on_message(filters.command("unmute") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to Unmute"
        )
    await message.chat.unban_member(user)
    await message.reply_text("Unmuted!")


# Ban deleted accounts


@app.on_message(filters.command("ban_ghosts"))
@adminsOnly("can_restrict_members")
async def ban_deleted_accounts(_, message: Message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    async for i in app.iter_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.kick_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await message.reply_text(f"Banned {banned_users} Deleted Accounts")
    else:
        await message.reply_text("There are no deleted accounts in this chat")


@app.on_message(filters.command("warn") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to warn a user.")
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id in SUDOERS:
        await message.reply_text("You Wanna Warn The Elevated One?")
    elif user_id == BOT_ID:
        await message.reply_text("Huh, Can't warn myself.")
    elif user_id in await list_admins(message.chat.id):
        await message.reply_text("Can't warn an admin.")
    else:
        if user_id in await list_members(chat_id):
            warns = await get_warn(chat_id, await int_to_alpha(user_id))
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🚨  Remove Warn  🚨",
                            callback_data=f"unwarn_{user_id}",
                        )
                    ]
                ]
            )
            if warns:
                warns = warns["warns"]
            else:
                warn = {"warns": 1}
                await add_warn(chat_id, await int_to_alpha(user_id), warn)
                return await message.reply_text(
                    f"Warned {mention} | 1/3 warnings now.",
                    reply_markup=keyboard,
                )
            if warns >= 2:
                await message.chat.kick_member(user_id)
                await message.reply_text(
                    f"Number of warns of {mention} exceeded, Banned!"
                )
                await remove_warns(chat_id, await int_to_alpha(user_id))
            else:
                warn = {"warns": warns + 1}

                await message.reply_text(
                    f"Warned {mention} | {warns+1}/3 warnings now.",
                    reply_markup=keyboard,
                )
                return await add_warn(
                    chat_id, await int_to_alpha(user_id), warn
                )
        else:
            await message.reply_text("This user isn't here.")


@app.on_callback_query(filters.regex("unwarn_"))
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("User has no warnings.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__Warn removed by {from_user.mention}__"
    await cq.message.edit(text)


# Rmwarns


@app.on_message(filters.command("rmwarns") & ~filters.edited)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to remove a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} have no warnings.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"Removed warnings of {mention}.")


# Warns


@app.on_message(filters.command("warns") & ~filters.edited)
@capture_err
async def check_warns(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to check a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention_user = message.reply_to_message.from_user.mention
    mention_from_user = message.from_user.mention
    chat_id = message.chat.id
    if message.reply_to_message:
        warns = await get_warn(chat_id, await int_to_alpha(user_id))
        if warns:
            warns = warns["warns"]
        else:
            return await message.reply_text(
                f"{mention_user} have no warnings."
            )
        return await message.reply_text(
            f"{mention_user} have {warns}/3 warnings."
        )
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention_user} have no warnings.")
    await message.reply_text(f"{mention_from_user} have {warns}/3 warnings.")


# Report


@app.on_message(
    filters.command(["report", "admins"], prefixes=["@", "/"])
    & ~filters.edited
)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to report user.")
    list_of_admins = await list_admins(message.chat.id)
    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention} to admins."
    for admin in list_of_admins:
        text += f"[\u2063](tg://user?id={admin})"
    await message.reply_text(text)
