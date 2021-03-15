from pyrogram import filters
from pyrogram.types import ChatPermissions
from wbb import OWNER_ID, SUDOERS, app
from wbb.utils.botinfo import BOT_ID
from wbb.utils.errors import capture_err

__MODULE__ = "Admin"
__HELP__ = '''/ban - Ban A User
/unban - Unban A User
/kick - Kick A User
/purge - Purge Messages
/del - Delete Replied Message
/promote - Promote A Member
/pin - Pin A Message
/mute - Mute A User
/unmute - Unmute A User
/ban_ghosts - Ban Deleted Accounts'''


async def list_admins(group_id):
    list_of_admins = []
    async for member in app.iter_chat_members(
            group_id, filter="administrators"):
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


# Kick members


@app.on_message(filters.command("kick") & ~filters.edited)
@capture_err
async def kick(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            if len(message.command) == 2:
                username = message.text.split(None, 1)[1]
                if (await app.get_users(username)).id in SUDOERS:
                    await message.reply_text("You Wanna Kick The Elevated One?")
                else:
                    if (await app.get_users(username)).id in \
                            await list_members(chat_id):
                        await message.chat.kick_member(username)
                        await message.chat.unban_member(username)
                        await message.reply_text(f"Kicked {username}")
                    else:
                        await message.reply_text("This user isn't here,"
                                                 " consider kicking yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                if user_id in SUDOERS:
                    await message.reply_text("You Wanna Kick The Elevated One?")
                else:
                    if user_id in await list_members(chat_id):
                        await message.reply_to_message.chat.kick_member(user_id)
                        await message.reply_to_message.chat.unban_member(user_id)
                        await message.reply_text("Kicked!")
                    else:
                        await message.reply_text("This user isn't here.")
    except Exception as e:
        await message.reply_text(str(e))

# Ban members


@app.on_message(filters.command("ban") & ~filters.edited)
@capture_err
async def ban(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            if len(message.command) == 2:
                username = message.text.split(None, 1)[1]
                if (await app.get_users(username)).id in SUDOERS:
                    await message.reply_text("You Wanna Ban The Elevated One?")
                else:
                    if (await app.get_users(username)).id in \
                            await list_members(chat_id):
                        await message.chat.kick_member(username)
                        await message.reply_text(f"Banned! {username}")
                    else:
                        await message.reply_text("This user isn't here,"
                                                 " consider banning yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                if user_id in SUDOERS:
                    await message.reply_text("You Wanna Ban The Elevated One?")
                else:
                    if user_id in await list_members(chat_id):
                        await message.reply_to_message.chat.kick_member(user_id)
                        await message.reply_text("Banned!")
                    else:
                        await message.reply_text("This user isn't here.")
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
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            if len(message.command) == 2:
                username = message.text.split(None, 1)[1]
                if (await app.get_users(username)).id not in \
                        await list_members(message.chat.id):
                    await message.chat.unban_member(username)
                    await message.reply_text(f"Unbanned! {username}")
                else:
                    await message.reply_text("This user is already here,"
                                             " consider banning yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                if user_id not in \
                        await list_members(chat_id):
                    await message.chat.unban_member(user_id)
                    await message.reply_text("Unbanned!")
                else:
                    await message.reply_text("This user is already here.")
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
        if "can_delete_messages" in permissions or from_user_id in SUDOERS:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.reply_text("You Don't Have Enough Permissions,"
                                     + " Consider Deleting Yourself!")
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
        if "can_promote_members" in permissions or from_user_id in SUDOERS:
            if len(message.command) == 2:
                username = message.text.split(None, 1)[1]
                user_id = (await app.get_users(username)).id
                await message.chat.promote_member(
                    user_id=user_id,
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=True)
                await message.reply_text('Promoted!')

            elif len(message.command) == 1 and message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                await message.chat.promote_member(
                    user_id=user_id,
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False, 
                    can_pin_messages=True, 
                    can_promote_members=True)
                await message.reply_text('Promoted!')
            else:
                await message.reply_text("Reply To A User's Message Or Give A Username To Promote.")

        else:
            await message.reply_text("You're Not An Admin, Want A Good Ban?")
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
    except Exception as e:
        await message.reply_text(str(e))


# Mute members


@app.on_message(filters.command("mute") & ~filters.edited)
@capture_err
async def mute(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A User's Message!")
        return
    try:
        chat_id = message.chat.id
        from_user_id = message.from_user.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            user_id = message.reply_to_message.from_user.id
            await message.chat.restrict_member(user_id,
                                               permissions=ChatPermissions())
            await message.reply_text("Muted!")
        else:
            await message.reply_text("Get Yourself An Admin Tag!")
    except Exception as e:
        await message.reply_text(str(e))

# Unmute members


@app.on_message(filters.command("unmute") & ~filters.edited)
@capture_err
async def unmute(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A User's Message!")
        return
    try:
        chat_id = message.chat.id
        from_user_id = message.from_user.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            user_id = message.reply_to_message.from_user.id
            await message.chat.unban_member(user_id)
            await message.reply_text("Unmuted!")
        else:
            await message.reply_text("Get Yourself An Admin Tag!")
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
