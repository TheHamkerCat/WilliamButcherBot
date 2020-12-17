import asyncio
from pyrogram import Client, filters
from wbb.utils import cust_filter
from wbb import app, Command

@app.on_message(cust_filter.command(commands=(["purge"])))
async def purge(client, message):
    app.set_parse_mode("markdown")
    if message.chat.type not in (("supergroup", "channel")):
        return

    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id,
            message.message_id
        ):
            message_ids.append(a_s_message_id)
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)

    status_message = await message.reply_text(
        f"```Purged!```"
    )
    await asyncio.sleep(5)
    await status_message.delete()
