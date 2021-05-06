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
from pyrogram.types import ChatPermissions
from wbb import SUDOERS, app, BOT_ID
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import add_warn, get_warn, remove_warns, int_to_alpha
import asyncio

__MODULE__ = "Admin"
__HELP__ = '''/ban - Ban A User
/unban - Unban A User
/warn - Warn A User
/rmwarns - Remove All Warning of A User
/warns - Show Warning Of A User
/kick - Kick A User
/purge - Purge Messages
/del - Delete Replied Message
/promote - Promote A Member
/pin - Pin A Message
/mute - Mute A User
/unmute - Unmute A User
/ban_ghosts - Ban Deleted Accounts
/report | @admins - Report A Message To Admins.'''


async def list_admins(chat_id):
    list_of_admins = []
    async for member in app.iter_chat_members(
            chat_id, filter="administrators"):
        list_of_admins.append(member.user.id)
    return list_of_admins


async def member_permissions(chat_id, user_id):
    perms = []
    member = (await app.get_chat_member(chat_id, user_id))
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
@capture_err
async def purge(client, message):
    try:
        message_ids = []
        chat_id = message.chat.id
        user_id = message.from_user.id
        if message.chat.type not in ("supergroup", "channel"):
            return
        permissions = await member_permissions(chat_id, user_id)
        if "can_delete_messages" in permissions or user_id in SUDOERS:
            if message.reply_to_message:
                for a_s_message_id in range(
                    message.reply_to_message.message_id,
                    message.message_id
                ):
                    message_ids.append(a_s_message_id)
                    if len(message_ids) == 100:
                        await client.delete_messages(chat_id=chat_id,
                                                     message_ids=message_ids,
                                                     revoke=True)
                        message_ids = []
                if len(message_ids) > 0:
                    await client.delete_messages(
                        chat_id=chat_id,
                        message_ids=message_ids,
                        revoke=True
                    )
            else:
                await message.reply_text(
                    "Reply To A Message To Delete It,"
                    " Don't Make Fun Of Yourself!")
        else:
            await message.reply_text("Your Don't Have Enough Permissions!")
        await message.delete()
    except Exception as e:
        print(e)
        await message.reply_text(e)

# Kick members


@app.on_message(filters.command("kick") & ~filters.edited)
@capture_err
async def kick(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Provide a username or reply to a user's message to kick.")
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Kick The Elevated One?")
        else:
            await message.reply_to_message.chat.kick_member(user_id)
            await asyncio.sleep(1)
            await message.reply_to_message.chat.unban_member(user_id)
            await message.reply_text("Kicked!")
    except Exception as e:
        print(e)
        await message.reply_text(e)

# Ban members


@app.on_message(filters.command("ban") & ~filters.edited)
@capture_err
async def ban(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Provide a username or reply to a user's message to ban.")
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Ban The Elevated One?")
        else:
            await message.chat.kick_member(user_id)
            await message.reply_text("Banned!")
    except Exception as e:
        await message.reply_text(str(e))


# Unban members


@app.on_message(filters.command("unban") & ~filters.edited)
@capture_err
async def unban(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user = message.text.split(None, 1)[1]
        elif len(message.command) == 1 and message.reply_to_message:
            user = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Provide a username or reply to a user's message to unban.")
            return
        await message.chat.unban_member(user)
        await message.reply_text("Unbanned!")
    except Exception as e:
        await message.reply_text(str(e))


# Delete messages


@app.on_message(filters.command("del") & ~filters.edited)
@capture_err
async def delete(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Delete It")
        return
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_delete_messages" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You Don't Have Enough Permissions,"
                                     + " Consider Deleting Yourself!")
            return
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await message.reply_text(str(e))

# Promote Members


@app.on_message(filters.command("promote") & ~filters.edited)
@capture_err
async def promote(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_promote_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions")
            return
        bot = await app.get_chat_member(chat_id, BOT_ID)
        if len(message.command) == 2:
            username = message.text.split(None, 1)[1]
            user_id = (await app.get_users(username)).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Reply To A User's Message Or Give A Username To Promote.")
            return
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats
        )
        await message.reply_text('Promoted!')

    except Exception as e:
        await message.reply_text(str(e))

# Pin Messages


@app.on_message(filters.command("pin") & ~filters.edited)
@capture_err
async def pin(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Pin.")
        return
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_pin_messages" in permissions or from_user_id in SUDOERS:
            await message.reply_to_message.pin(disable_notification=True)
        else:
            await message.reply_text("You're Not An Admin, Stop Spamming!")
            return
    except Exception as e:
        await message.reply_text(str(e))


# Mute members


@app.on_message(filters.command("mute") & ~filters.edited)
@capture_err
async def mute(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Provide a username or reply to a user's message to mute.")
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Mute The Elevated One?")
            return
        await message.chat.restrict_member(
            user_id,
            permissions=ChatPermissions()
        )
        await message.reply_text("Muted!")
    except Exception as e:
        await message.reply_text(str(e))

# Unmute members


@app.on_message(filters.command("unmute") & ~filters.edited)
@capture_err
async def unmute(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" not in permissions and from_user_id not in SUDOERS:
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user = message.text.split(None, 1)[1]
        elif len(message.command) == 1 and message.reply_to_message:
            user = message.reply_to_message.from_user.id
        else:
            await message.reply_text("Provide a username or reply to a user's message to Unmute")
            return
        await message.chat.unban_member(user)
        await message.reply_text("Unmuted!")
    except Exception as e:
        await message.reply_text(str(e))


# Ban deleted accounts


@app.on_message(filters.command("ban_ghosts"))
async def ban_deleted_accounts(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            deleted_users = []
            banned_users = 0
            async for i in app.iter_chat_members(chat_id):
                if i.user.is_deleted:
                    deleted_users.append(i.user.id)
            if len(deleted_users) > 0:
                for deleted_user in deleted_users:
                    try:
                        await message.chat.kick_member(deleted_user)
                    except Exception as e:
                        print(str(e))
                        pass
                    banned_users += 1
                await message.reply_text(f"Banned {banned_users} Deleted Accounts")
            else:
                await message.reply_text("No Deleted Accounts In This Chat")
                return
        else:
            await message.reply_text("You Don't Have Enough Permissions")
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))


@app.on_message(filters.command("warn") & ~filters.edited)
@capture_err
async def warn_user(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to warn a user.")
        return
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            user_id = message.reply_to_message.from_user.id
            mention = message.reply_to_message.from_user.mention
            if user_id in SUDOERS:
                await message.reply_text("You Wanna Warn The Elevated One?")
            elif user_id == BOT_ID:
                await message.reply_text("Huh, Can't warn myself.")
            elif user_id in await list_admins(message.chat.id):
                await message.reply_text("Can't warn an admin.")
            elif user_id == from_user_id:
                await message.reply_text("I wouldn't do that if i were you.")
            else:
                if user_id in await list_members(chat_id):
                    warns = await get_warn(chat_id, await int_to_alpha(user_id))
                    if warns:
                        warns = warns['warns']
                    else:
                        warn = {"warns": 1}
                        await add_warn(chat_id, await int_to_alpha(user_id), warn)
                        await message.reply_text(f"Warned {mention} !, 1/3 warnings now.")
                        return
                    if warns >= 2:
                        await message.chat.kick_member(user_id)
                        await message.reply_text(f"Number of warns of {mention} exceeded, Banned!")
                        await remove_warns(chat_id, await int_to_alpha(user_id))
                    else:
                        warn = {"warns": warns+1}
                        await add_warn(chat_id, await int_to_alpha(user_id), warn)
                        await message.reply_text(f"Warned {mention} !, {warns+1}/3 warnings now.")
                else:
                    await message.reply_text("This user isn't here.")
        else:
            await message.reply_text("You don't have enough permissions.")
    except Exception as e:
        await message.reply_text(str(e))


# Rmwarns


@app.on_message(filters.command("rmwarns") & ~filters.edited)
@capture_err
async def remove_warnings(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to remove a user's warnings.")
        return
    try:
        from_user_id = message.from_user.id
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            warns = await get_warn(chat_id, await int_to_alpha(user_id))
            if warns:
                warns = warns['warns']
            if warns == 0 or not warns:
                await message.reply_text(f"{mention} have no warnings.")
            else:
                await remove_warns(chat_id, await int_to_alpha(user_id))
                await message.reply_text(f"Removed warnings of {mention}.")
        else:
            await message.reply_text("You don't have enough permissions")
    except Exception as e:
        await message.reply_text(str(e))


# Warns


@app.on_message(filters.command("warns") & ~filters.edited)
@capture_err
async def check_warns(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to check a user's warnings.")
        return
    try:
        user_id = message.reply_to_message.from_user.id
        mention_user = message.reply_to_message.from_user.mention
        mention_from_user = message.from_user.mention
        chat_id = message.chat.id
        if message.reply_to_message:
            warns = await get_warn(chat_id, await int_to_alpha(user_id))
            if warns:
                warns = warns['warns']
            else:
                await message.reply_text(f"{mention_user} have no warnings.")
                return
            await message.reply_text(f"{mention_user} have {warns}/3 warnings.")
            return
        warns = await get_warn(chat_id, await int_to_alpha(user_id))
        if warns:
            warns = warns['warns']
        else:
            await message.reply_text(f"{mention_user} have no warnings.")
            return
        await message.reply_text(f"{mention_from_user} have {warns}/3 warnings.")
    except Exception as e:
        await message.reply_text(str(e))

# Report


@app.on_message(filters.command(["report", "admins"], prefixes=["@", "/"]) & ~filters.edited)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to report user.")
        return
    list_of_admins = await list_admins(message.chat.id)
    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention} to admins."
    for admin in list_of_admins:
        text += f"[\u2063](tg://user?id={admin})"
    await message.reply_text(text)
