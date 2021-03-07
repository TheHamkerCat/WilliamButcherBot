from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from wbb import OWNER_ID, SUDO_USER_ID, app
from wbb.utils import cust_filter
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
/unmute - Unmute A User'''

SUDO = [OWNER_ID, SUDO_USER_ID]

# Get List Of Admins In A Chat


async def list_admins(group_id):
    list_of_admins = []
    async for member in app.iter_chat_members(
            group_id, filter="administrators"):
        list_of_admins.append(member.user.id)
    return list_of_admins

# Get List Of Members In A Chat


async def list_members(group_id):
    list_of_members = []
    async for member in app.iter_chat_members(group_id):
        list_of_members.append(member.user.id)
    return list_of_members

# Purge Messages


@app.on_message(cust_filter.command(commands=("purge")) & ~filters.edited)
@capture_err
async def purge(client, message: Message):
    message_ids = []
    if message.chat.type not in ("supergroup", "channel"):
        return

    admins = await list_admins(message.chat.id)

    if message.from_user.id in admins \
            or message.from_user.id in SUDO:

        chat_id = message.chat.id
        from_user_id = message.from_user.id
        if (await app.get_chat_member(chat_id,
                                      from_user_id)).can_delete_messages \
                or (await app.get_chat_member(chat_id, from_user_id)).status \
                == 'creator' \
                or message.from_user.id in SUDO:

            if message.reply_to_message:
                for a_s_message_id in range(
                    message.reply_to_message.message_id,
                    message.message_id
                ):
                    message_ids.append(a_s_message_id)
                    if len(message_ids) == 100:
                        await client.delete_messages(
                            chat_id=message.chat.id,
                            message_ids=message_ids,
                            revoke=True
                        )
                        message_ids = []
                if len(message_ids) > 0:
                    await client.delete_messages(
                        chat_id=message.chat.id,
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


@app.on_message(cust_filter.command(commands=("kick")) & ~filters.edited)
@capture_err
async def kick(_, message: Message):
    try:
        if (await app.get_chat_member(
            message.chat.id, message.from_user.id)).status == 'creator' \
            or (await app.get_chat_member(
                message.chat.id, message.from_user.id)).can_restrict_members \
                is True or message.from_user.id in SUDO:

            if len(message.command) == 2:
                username = (message.text.split(None, 1)[1])
                if (await app.get_users(username)).id in SUDO:
                    await message.reply_text("You Wanna Kick The Elevated One?")
                else:
                    if (await app.get_users(username)).id in \
                            await list_members(message.chat.id):
                        await message.chat.kick_member(username)
                        await message.chat.unban_member(username)
                        await message.reply_text(f"Kicked {username}")
                    else:
                        await message.reply_text("This user isn't here,"
                                                 " consider kicking yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                if message.reply_to_message.from_user.id in SUDO:
                    await message.reply_text("You Wanna Kick The Elevated One?")
                else:
                    if message.reply_to_message.from_user.id in \
                            await list_members(message.chat.id):
                        user_id = message.reply_to_message.from_user.id
                        await message.reply_to_message.chat.kick_member(user_id)
                        await message.reply_to_message.chat.unban_member(user_id)
                        await message.reply_text("Kicked!")
                    else:
                        await message.reply_text("This user isn't here.")
    except Exception as e:
        await message.reply_text(str(e))

# Ban members


@app.on_message(cust_filter.command(commands=("ban")) & ~filters.edited)
@capture_err
async def ban(_, message: Message):
    try:
        if (await app.get_chat_member(
            message.chat.id, message.from_user.id)).status == 'creator' \
            or (await app.get_chat_member(
                message.chat.id, message.from_user.id)).can_restrict_members \
                is True or message.from_user.id in SUDO:

            if len(message.command) == 2:
                username = (message.text.split(None, 1)[1])
                if (await app.get_users(username)).id in SUDO:
                    await message.reply_text("You Wanna Ban The Elevated One?")
                else:
                    if (await app.get_users(username)).id in \
                            await list_members(message.chat.id):
                        await message.chat.kick_member(username)
                        await message.reply_text(f"Banned! {username}")
                    else:
                        await message.reply_text("This user isn't here,"
                                                 " consider banning yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                if message.reply_to_message.from_user.id in SUDO:
                    await message.reply_text("You Wanna Ban The Elevated One?")
                else:
                    if message.reply_to_message.from_user.id in \
                            await list_members(message.chat.id):
                        user_id = message.reply_to_message.from_user.id
                        await message.reply_to_message.chat.kick_member(user_id)
                        await message.reply_text("Banned!")
                    else:
                        await message.reply_text("This user isn't here.")
    except Exception as e:
        await message.reply_text(str(e))


# Unban members


@app.on_message(cust_filter.command(commands=("unban")) & ~filters.edited)
@capture_err
async def unban(_, message: Message):
    try:
        if (await app.get_chat_member(
            message.chat.id, message.from_user.id)).status == 'creator' \
            or (await app.get_chat_member(
                message.chat.id, message.from_user.id)).can_restrict_members \
                is True or message.from_user.id in SUDO:

            if len(message.command) == 2:
                username = (message.text.split(None, 1)[1])
                if (await app.get_users(username)).id not in \
                        await list_members(message.chat.id):
                    await message.chat.unban_member(username)
                    await message.reply_text(f"Unbanned! {username}")
                else:
                    await message.reply_text("This user is already here,"
                                             " consider banning yourself.")

            if len(message.command) == 1 and message.reply_to_message:
                if message.reply_to_message.from_user.id not in \
                        await list_members(message.chat.id):
                    user_id = message.reply_to_message.from_user.id
                    await message.chat.unban_member(user_id)
                    await message.reply_text("Unbanned!")
                else:
                    await message.reply_text("This user is already here.")
    except Exception as e:
        await message.reply_text(str(e))


# Delete messages


@app.on_message(cust_filter.command(commands=("del")))
@capture_err
async def delete(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Delete It")
        return
    try:
        admins = await list_admins(message.chat.id)
        chat_id = message.chat.id
        from_user_id = message.from_user.id

        if message.from_user.id in admins \
                or message.from_user.id in SUDO:
            if (await app.get_chat_member(chat_id,
                                          from_user_id)).can_delete_messages \
                or (await app.get_chat_member(chat_id, from_user_id)).status \
                == 'creator' \
                    or message.from_user.id in SUDO:
                await message.reply_to_message.delete()
                await message.delete()
        else:
            await message.reply_text("You Don't Have Enough Permissions,"
                                     + " Consider Wiping Yourself Off The Existence!")
    except Exception as e:
        await message.reply_text(str(e))

# Promote Members


@app.on_message(cust_filter.command(commands=("promote")) & ~filters.edited)
@capture_err
async def promote(_, message: Message):
    try:
        admins = await list_admins(message.chat.id)
        chat_id = message.chat.id
        from_user_id = message.from_user.id

        if (await app.get_chat_member(chat_id,
                                      BOT_ID)).can_promote_members:
            if message.from_user.id in admins \
                    or message.from_user.id in SUDO:
                if (await app.get_chat_member(chat_id,
                                              from_user_id)).can_promote_members \
                    or (await app.get_chat_member(chat_id, from_user_id)).status \
                    == 'creator' \
                        or message.from_user.id in SUDO:

                    if not message.reply_to_message and len(message.command) == 2:
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

                    elif message.reply_to_message:
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
                    await message.reply_text("Yeah, I Can See You're An Admin,"
                                             + " But You Don't Have Permissions"
                                             + " To Promote Someone.")
            else:
                await message.reply_text("You're Not An Admin, Want A Good Ban?")
        else:
            await message.reply_text("Well, Your Know What?, I'M NOT AN ADMIN!"
                                     + " MAKE ME ADMIN!")
    except Exception as e:
        await message.reply_text(str(e))

# Pin Messages


@app.on_message(cust_filter.command(commands=("pin")) & ~filters.edited)
@capture_err
async def pin(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Pin.")
        return
    try:
        admins = await list_admins(message.chat.id)
        chat_id = message.chat.id
        from_user_id = message.from_user.id

        if message.from_user.id in admins \
                or message.from_user.id in SUDO:
            if (await app.get_chat_member(chat_id,
                                          from_user_id)).can_pin_messages \
                or (await app.get_chat_member(chat_id, from_user_id)).status \
                == 'creator' \
                    or message.from_user.id in SUDO:

                await message.reply_to_message.pin(disable_notification=True)
        else:
            await message.reply_text("You're Not An Admin, Stop Spamming!")
    except Exception as e:
        await message.reply_text(str(e))


# Mute members


@app.on_message(cust_filter.command(commands=("mute")) & ~filters.edited)
@capture_err
async def mute(_, message: Message):
    try:
        chat_id = message.chat.id
        from_user_id = message.from_user.id
        if not message.reply_to_message:
            await message.reply_text("Reply To A User's Message!")
            return

        if (await app.get_chat_member(chat_id,
                                      from_user_id)).can_restrict_members \
            or (await app.get_chat_member(chat_id, from_user_id)).status \
            == 'creator' \
                or message.from_user.id in SUDO:
            victim = message.reply_to_message.from_user.id
            await message.chat.restrict_member(victim,
                                               permissions=ChatPermissions())
            await message.reply_text("Muted!")
        else:
            await message.reply_text("Get Yourself An Admin Tag!")
    except Exception as e:
        await message.reply_text(str(e))

# Unmute members


@app.on_message(cust_filter.command(commands=("unmute")) & ~filters.edited)
@capture_err
async def unmute(_, message: Message):
    try:
        chat_id = message.chat.id
        from_user_id = message.from_user.id
        if not message.reply_to_message:
            await message.reply_text("Reply To A User's Message!")
            return
        if (await app.get_chat_member(chat_id,
                                      from_user_id)).can_restrict_members \
            or (await app.get_chat_member(chat_id, from_user_id)).status \
            == 'creator' \
                or message.from_user.id in SUDO:
            victim = message.reply_to_message.from_user.id
            await message.chat.unban_member(victim)
            await message.reply_text("Unmuted!")
        else:
            await message.reply_text("Get Yourself An Admin Tag!")
    except Exception as e:
        await message.reply_text(str(e))
