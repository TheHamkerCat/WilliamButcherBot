from wbb import app
from wbb.utils.filter_groups import global_stats_group
from wbb.utils.errors import capture_err
from wbb.utils.botinfo import BOT_ID, BOT_NAME
from wbb.utils.dbfunctions import (
        is_served_chat,
        get_served_chats,
        add_served_chat,
        remove_served_chat,
        alpha_to_int
        )
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


@app.on_message(filters.new_chat_members & filters.left_chat_member)
@capture_err
async def chat_watcher(_, message):
    chat_id = message.chat.id
    served_chat = await is_served_chat(chat_id)
    if served_chat:
        return
    await add_served_chat(chat_id)


@app.on_message(filters.command("/global_stats") & ~filters.edited)
@capture_err
async def global_stats(_, message):
    m = await message.reply_text("__**Analysing Stats, Might Take 10-30 Seconds.**__")
    served_chats = []
    total_users = 0
    chats = await get_served_chats 
    for chat in chats:
        served_chats.append(await alpha_to_int(chat))
    for served_chat in served_chats:
        try:
            await app.get_chat_member(served_chat, BOT_ID)
        except UserNotParticipant:
            await remove_served_chat(served_chat)
            served_chats.remove(served_chat)
            pass
    for i in served_chats:
        total_users += int((await app.get_chat(i)).members_count)
    msg = f"""**Global Stats of {BOT_NAME}**:
0 gbanned users.
0 blacklist triggers, across 0 chats.
0 filters, across 0 chats.
0 notes, across 0 chats.
0 welcome messages are set.
{total_users} users, across {len(served_chats)} chats.
0 warns, across 0 chats.
0 """
    await m.edit(msg)



