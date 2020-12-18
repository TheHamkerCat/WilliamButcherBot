import asyncio
from wbb.utils import cust_filter
from wbb import app
from wbb.utils.is_admin import is_admin


__MODULE__ = "Admin"
__HELP__ = '''
/purge - Purge Messages [Limit = 100]

'''


@app.on_message(cust_filter.command(commands=("purge")))
async def purge(client, message):
    app.set_parse_mode("markdown")
    if message.chat.type not in (("supergroup", "channel")):
        return
    admin = await is_admin(message)

    if not admin:
        return

    message_ids = []

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

    m = await message.reply_text(
        "```Purged!```"
    )
    await asyncio.sleep(2)
    await m.delete()
