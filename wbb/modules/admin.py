from wbb import OWNER_ID, SUDO_USER_ID, app
from wbb.utils import cust_filter, botinfo


__MODULE__ = "Admin"
__HELP__ = "/purge - Purge Messages\n" \
            "/kick - Kick A User\n" \
            "/ban - Ban A User\n" \
            "/unban - Unban A User"

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


@app.on_message(cust_filter.command(commands=("purge")))
async def purge(client, message):
    message_ids = []
    if message.chat.type not in (("supergroup", "channel")):
        return

    admins = await list_admins(message.chat.id)

    if message.from_user.id in admins \
            or message.from_user.id in SUDO:

        if (await app.get_chat_member(
                message.chat.id, message.from_user.id
                )).can_delete_messages is True \
                or (await app.get_chat_member(            # Flake8 Hoe
                    message.chat.id, message.from_user.id
                    )).status == 'creator' \
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


# Kick members


@app.on_message(cust_filter.command(commands=("kick")))
async def kick(client, message):
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
                                             " don't bully me!")

        else:
            if username in SUDO or message.reply_to_message.from_user.id \
             in SUDO:
                await message.reply_text("You Wanna Kick The Elevated One?")
            else:
                if message.reply_to_message.from_user.id in \
                await list_members(message.chat.id):
                    id = message.reply_to_message.from_user.id
                    await message.reply_to_message.chat.kick_member(id)
                    await message.reply_to_message.chat.unban_member(id)
                    await message.reply_text(f"Kicked {username}")
                else:
                    await message.reply_text("This user isn't here,"
                                             " don't bully me!")

# Ban members


@app.on_message(cust_filter.command(commands=("ban")))
async def ban(client, message):
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
                                             " don't bully me!")
        else:
            if username in SUDO or message.reply_to_message.from_user.id \
             in SUDO:
                await message.reply_text("You Wanna Ban The Elevated One?")
            else:
                if (await app.get_users(username)).id in \
                await list_members(message.chat.id):
                    id = message.reply_to_message.from_user.id
                    await message.reply_to_message.chat.kick_member(id)
                    await message.reply_text(f"Banned {username}")
                else:
                    await message.reply_text("This user isn't here,"
                                             " don't bully me!")

# Unban members


@app.on_message(cust_filter.command(commands=("unban")))
async def unban(client, message):
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
                await message.chat.kick_member(username)
                await message.reply_text(f"Unbanned {username}")
            else:
                await message.reply_text("This user is already here,"
                                             " don't bully me!")


        else:
            if (await app.get_users(username)).id not in \
            await list_members(message.chat.id):
                id = message.reply_to_message.from_user.id
                await message.reply_to_message.chat.kick_member(id)
                await message.reply_text(f"Unbanned {username}")
            else:
                await message.reply_text("This user is already here,"
                                             " don't bully me!")

# Kick members on their own call
@app.on_message(cust_filter.command(commands=("kickme")))
async def kickme(client, message):
    await message.chat.kick_member(message.from_user.id)
    await message.chat.unban_member(message.from_user.id)
    await message.reply_text("Joke's on you, i'm into that shit")

# Ban members on their own call
@app.on_message(cust_filter.command(commands=("kickme")))
async def kickme(client, message):
    await message.chat.kick_member(message.from_user.id)
    await message.chat.unban_member(message.from_user.id)
    await message.reply_text("Joke's on you, i'm into that shit")
