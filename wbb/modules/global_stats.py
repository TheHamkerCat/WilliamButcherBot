from wbb import app
from wbb.utils.filter_groups import global_stats_group
from wbb.utils.errors import capture_err
from wbb.utils.botinfo import BOT_ID, BOT_NAME
from wbb.utils.dbfunctions import (
        is_served_chat,
        get_served_chats,
        add_served_chat,
        remove_served_chat,
        get_notes_count,
        get_filters_count,
        get_warns_count
        )
from pyrogram import filters

@app.on_message(filters.text, group=global_stats_group)
@capture_err
async def chat_watcher(_, message):
    chat_id = message.chat.id
    served_chat = await is_served_chat(chat_id)
    if served_chat: return
    await add_served_chat(chat_id)


@app.on_message(filters.command("global_stats") & ~filters.edited)
@capture_err
async def global_stats(_, message):
    m = await app.send_message(
            message.chat.id,
            text="__**Analysing Stats, Might Take 10-30 Seconds.**__")
    
    ## For bot served chat and users count

    served_chats = []
    total_users = 0
    chats = await get_served_chats()
    for chat in chats: served_chats.append(chat["chat_id"])
    for served_chat in served_chats:
        try: await app.get_chat_member(served_chat, BOT_ID)
        except Exception:
            await remove_served_chat(served_chat)
            served_chats.remove(served_chat)
            pass
    for i in served_chats:
        mc = (await app.get_chat(i)).members_count
        total_users += int(mc)
    
    ## For notes count across chats
    _notes = await get_notes_count()
    notes_count = _notes["notes_count"]
    notes_chats_count = _notes["chats_count"]

    # For filters count across chats
    _filters = await get_filters_count()
    filters_count = _filters["filters_count"]
    filters_chats_count = _filters["chats_count"]
    
    # For warns count across chats
    _warns = await get_warns_count()
    warns_count = _warns["warns_count"]
    warns_chats_count = _warns["chats_count"]
    # NOTE need to fix these
    msg = f"""**Global Stats of {BOT_NAME}**:
0 gbanned users.                           
0 blacklist triggers, across 0 chats.
{filters_count} filters, across {filters_chats_count} chats.
{notes_count} notes, across {notes_chats_count} chats.
0 welcome messages are set.
{total_users} users, across {len(served_chats)} chats.
{warns_count} warns, across {warns_chats_count} chats."""
    
    await m.edit(msg)

