import asyncio
from wbb.utils import cust_filter
from wbb import app, OWNER_ID


__MODULE__ = "Admin"
__HELP__ = "/purge - Purge Messages [Limit = 100]"

# Purge Messages


@app.on_message(cust_filter.command(commands=("purge")))
async def purge(client, message):
    if message.chat.type not in (("supergroup", "channel")):
        return

    message_ids = []
    # Admin check logic
    group_id = message.chat.id
    list_of_admins = []
    async for member in app.iter_chat_members(
            group_id, filter="administrators"):
        list_of_admins.append(member.user.id)

    if message.from_user.id in list_of_admins \
            or message.from_user.id == OWNER_ID:
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

        m = await message.reply_text("Purged!")
        await asyncio.sleep(1)
        await m.delete()

    else:
        await message.reply_text("You Are Not Admin, Stop Spamming! else /bun")

# Kicking users


@app.on_message(cust_filter.command(commands=("kick")))
async def kick(client, message):
    username = (message.text.split(None, 1)[1])
    if username != "":
        



