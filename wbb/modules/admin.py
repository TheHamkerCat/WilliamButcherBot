from wbb import OWNER_ID, SUDO_USER_ID, app
from wbb.utils import cust_filter


__MODULE__ = "Admin"
__HELP__ = "/purge - Purge Messages"

SUDO = [OWNER_ID, SUDO_USER_ID]

# Get The List Of Admins In A Chats


async def list_admins(group_id):
    list_of_admins = []
    async for member in app.iter_chat_members(
            group_id, filter="administrators"):
        list_of_admins.append(member.user.id)
    return list_of_admins


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
    username = (message.text.split(None, 2)[1])
    reason = (message.text.split(None, 2)[2])

    admins = await list_admins(message.chat.id)

    if message.from_user.id in admins \
            or message.from_user.id in SUDO:
        if username != "":
            await message.chat.kick_member(username)
            await message.chat.unban_member(username)

            if reason != "":
                await message.reply_text(
                    f"Kicked {username}!"
                    f"Reason: {reason}")
            else:
                await message.reply_text(
                    f"Kicked {username}!"
                    f"Reason: Kicked without a reason! lol")

        else:
            id = message.reply_to_message.from_user.id
            await message.reply_to_message.chat.kick_member(id)
            await message.reply_to_message.chat.unban_member(id)

            if reason != "":
                await message.reply_text(
                    f"Kicked {username}!"
                    f"Reason: {reason}")
            else:
                await message.reply_text(
                    f"Kicked {username}!"
                    f"Reason: Kicked without a reason! lol")
    else:
        await message.reply_text("You Are Not Admin, Stop Spamming! else /bun")


# Ban members


@app.on_message(cust_filter.command(commands=("ban")))
async def ban(client, message):
    username = (message.text.split(None, 1)[1])
    if username != "":
        await message.chat.kick_member(username)
        await message.reply_text(f"Banned {username}!")
    else:
        id = message.reply_to_message.from_user.id
        await message.reply_to_message.chat.kick_member(id)
        await message.reply_text(f"Banned {username}!")

# Unban members


@app.on_message(cust_filter.command(commands=("unban")))
async def unban(client, message):
    username = (message.text.split(None, 1)[1])
    if username != "":
        await message.chat.unban_member(username)
        await message.reply_text(f"Unbanned {username}!")
    else:
        id = message.reply_to_message.from_user.id
        await message.reply_to_message.chat.unban_member(id)
        await message.reply_text(f"Unbanned {username}!")
