from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from wbb import OWNER_ID, SUDO_USER_ID, app
from wbb.utils import cust_filter
from wbb.utils.botinfo import BOT_ID

__MODULE__ = "Admin"
__HELP__ = '''/ban    - Ban A User
/unban  - Unban A User
/kick   - Kick A User
/purge  - Purge Messages
/del    - Delete Replied Message
/banme  - Bans A User Who Issued The Command
/kickme - Kicks A User Who Issued The Command
/promote - Promote A Member
/pin - Pin A Message
/unpin - Unpin A Message
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
async def kick(_, message: Message):
    try:
        username = (message.text.split(None, 2)[1])
    except IndexError:
        username = ""
    if (await app.get_chat_member(
        message.chat.id, message.from_user.id)).status == 'creator' \
        or (await app.get_chat_member(
            message.chat.id, message.from_user.id)).can_restrict_members \
            is True or message.from_user.id in SUDO:

        if username != "":
            if username in SUDO or (await app.get_users(username)).id in SUDO:
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

        else:
            if username in SUDO or message.reply_to_message.from_user.id \
                    in SUDO:
                await message.reply_text("You Wanna Kick The Elevated One?")
            else:
                if message.reply_to_message.from_user.id in \
                        await list_members(message.chat.id):
                    user_id = message.reply_to_message.from_user.id
                    await message.reply_to_message.chat.kick_member(user_id)
                    await message.reply_to_message.chat.unban_member(user_id)
                    await message.reply_text(f"Kicked {username}")
                else:
                    await message.reply_text("This user isn't here,"
                                             " consider kicking yourself.")

# Ban members


@app.on_message(cust_filter.command(commands=("ban")) & ~filters.edited)
async def ban(_, message: Message):
    try:
        username = (message.text.split(None, 2)[1])
    except IndexError:
        username = ""
    if (await app.get_chat_member(
        message.chat.id, message.from_user.id)).status == 'creator' \
        or (await app.get_chat_member(
            message.chat.id, message.from_user.id)).can_restrict_members \
            is True or message.from_user.id in SUDO:

        if username != "":
            if username in SUDO or (await app.get_users(username)).id in SUDO:
                await message.reply_text("You Wanna Ban The Elevated One?")
            else:
                if (await app.get_users(username)).id in \
                        await list_members(message.chat.id):
                    await message.chat.kick_member(username)
                    await message.reply_text(f"Banned {username}")
                else:
                    await message.reply_text("This user isn't here,"
                                             " consider banning yourself.")
        else:
            if username in SUDO or message.reply_to_message.from_user.id \
                    in SUDO:
                await message.reply_text("You Wanna Ban The Elevated One?")
            else:
                if (await app.get_users(username)).id in \
                        await list_members(message.chat.id):
                    user_id = message.reply_to_message.from_user.id
                    await message.reply_to_message.chat.kick_member(user_id)
                    await message.reply_text(f"Banned {username}")
                else:
                    await message.reply_text("This user isn't here,"
                                             " consider kicking yourself.")

# Unban members


@app.on_message(cust_filter.command(commands=("unban")) & ~filters.edited)
async def unban(_, message: Message):
    try:
        username = (message.text.split(None, 2)[1])
    except IndexError:
        username = ""
    if (await app.get_chat_member(
        message.chat.id, message.from_user.id)).status == 'creator' \
        or (await app.get_chat_member(
            message.chat.id, message.from_user.id)).can_restrict_members \
            is True or message.from_user.id in SUDO:

        if username != "":
            if (await app.get_users(username)).id not in \
                    await list_members(message.chat.id):
                await message.chat.unban_member(username)
                await message.reply_text(f"Unbanned {username}")
            else:
                await message.reply_text("This user is already here,"
                                         " don't bully me!")
        else:
            if (await app.get_users(username)).id not in \
                    await list_members(message.chat.id):
                user_id = message.reply_to_message.from_user.id
                await message.reply_to_message.chat.unban_member(user_id)
                await message.reply_text(f"Unbanned {username}")
            else:
                await message.reply_text("This user is already here,"
                                         " don't bully me!")

# Kick members on their own call


@app.on_message(cust_filter.command(commands=("kickme")) & ~filters.edited)
async def kickme(_, message: Message):
    if message.from_user.id not in SUDO:
        await message.chat.kick_member(message.from_user.id)
        await message.chat.unban_member(message.from_user.id)
        await message.reply_text("Kicked!, Joke's on you, I'm into that shit!")
    else:
        await message.reply_text("It doesn't works that way mate.")

# Ban members on their own call


@app.on_message(cust_filter.command(commands=("banme")))
async def banme(_, message: Message):
    if message.from_user.id not in SUDO:
        await message.chat.kick_member(message.from_user.id)
        await message.reply_text("Banned!, Joke's on you, I'm into that shit!")
    else:
        await message.reply_text("It doesn't works that way mate.")

# Delete messages


@app.on_message(cust_filter.command(commands=("del")))
async def delete(_, message: Message):
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
                                 + " Consider Deleting Yourself!")

# Promote Members


@app.on_message(cust_filter.command(commands=("promote")) & ~filters.edited)
async def promote(_, message: Message):
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

                if message.text != '/promote':
                    username = message.text.replace('/promote', '')
                    user_id = (await app.get_users(username)).id
                    await message.chat.promote_member(
                        user_id=user_id,
                        can_change_info=True,
                        can_invite_users=True,
                        can_restrict_members=True,
                        can_delete_messages=True,
                        can_pin_messages=True,
                        can_promote_members=True)
                    await message.reply_text('Promoted!')

                else:
                    user_id = message.reply_to_message.from_user.id
                    await message.chat.promote_member(
                        user_id=user_id,
                        can_change_info=True,
                        can_invite_users=True,
                        can_restrict_members=True,
                        can_delete_messages=True,
                        can_pin_messages=True,
                        can_promote_members=True)
                    await message.reply_text('Promoted!')

            else:
                await message.reply_text("Yeah, I Can See You're An Admin,"
                                         + " But You Don't Have Permissions"
                                         + " To Promote Someone.")
        else:
            await message.reply_text("You're Not An Admin, Want A Good Ban?")
    else:
        await message.reply_text("Well, Your Know What?, I'M NOT AN ADMIN!"
                                 + " MAKE ME ADMIN!")

# Pin Messages


@app.on_message(cust_filter.command(commands=("pin")) & ~filters.edited)
async def pin(_, message: Message):
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

            await message.reply_to_message.pin()
    else:
        await message.reply_text("You're Not An Admin, Stop Spamming!")

# Unpin Messages


@app.on_message(cust_filter.command(commands=("unpin")) & ~filters.edited)
async def unpin(_, message: Message):
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
            await app.unpin_all_chat_messages(chat_id)
    else:
        await message.reply_text("You're Not An Admin, Stop Spamming!")


@app.on_message(cust_filter.command(commands=("mute")) & ~filters.edited)
async def mute(_, message: Message):
    chat_id = message.chat.id
    admins = await list_admins(chat_id)
    from_user_id = message.from_user.id
    username = message.text.replace("/mute", "")

    if from_user_id in admins or from_user_id in SUDO:
        if username != "":
            victim = username
        else:
            victim = message.reply_to_message.from_user.id
        await message.chat.restrict_member(victim,
                                           permissions=ChatPermissions())
        await message.reply_text("Muted!")
    else:
        await message.reply_text("Get Yourself An Admin Tag!")


@app.on_message(cust_filter.command(commands=("unmute")) & ~filters.edited)
async def unmute(_, message: Message):
    chat_id = message.chat.id
    admins = await list_admins(chat_id)
    from_user_id = message.from_user.id
    username = message.text.replace("/unmute", "")

    if from_user_id in admins or from_user_id in SUDO:
        if username != "":
            victim = username
        else:
            victim = message.reply_to_message.from_user.id
        await message.chat.unban_member(victim)
        await message.reply_text("Unmuted!")
    else:
        await message.reply_text("Get Yourself An Admin Tag!")
