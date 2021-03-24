from wbb import app, SUDOERS
from wbb.utils.filter_groups import global_stats_group
from wbb.utils.errors import capture_err
from wbb.utils.botinfo import BOT_ID, BOT_NAME
from wbb.utils.fetch import fetch
from wbb.utils.dbfunctions import (
    is_served_chat,
    get_served_chats,
    add_served_chat,
    remove_served_chat,
    get_notes_count,
    get_filters_count,
    get_warns_count,
    get_karmas_count,
    get_gbans_count
)
from pyrogram import filters


@app.on_message(filters.text, group=global_stats_group)
@capture_err
async def chat_watcher(_, message):
    chat_id = message.chat.id
    served_chat = await is_served_chat(chat_id)
    if served_chat:
        return
    await add_served_chat(chat_id)


@app.on_message(
    filters.command("global_stats") & filters.user(SUDOERS)
    & ~filters.edited
)
@capture_err
async def global_stats(_, message):
    m = await app.send_message(
        message.chat.id,
        text="__**Analysing Stats, Might Take 10-30 Seconds.**__",
        disable_web_page_preview=True
    )

    # For bot served chat and users count
    served_chats = []
    total_users = 0
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    for served_chat in served_chats:
        try:
            await app.get_chat_members(served_chat, BOT_ID)
        except Exception as e:
            print(f"{e} - {served_chat} in global_stats.py")
            await remove_served_chat(served_chat)
            served_chats.remove(served_chat)
            pass
    for i in served_chats:
        mc = (await app.get_chat(i)).members_count
        total_users += int(mc)

    # Gbans count
    gbans = await get_gbans_count()
    # Notes count across chats
    _notes = await get_notes_count()
    notes_count = _notes["notes_count"]
    notes_chats_count = _notes["chats_count"]

    # Filters count across chats
    _filters = await get_filters_count()
    filters_count = _filters["filters_count"]
    filters_chats_count = _filters["chats_count"]

    # Warns count across chats
    _warns = await get_warns_count()
    warns_count = _warns["warns_count"]
    warns_chats_count = _warns["chats_count"]

    # Karmas count across chats
    _karmas = await get_karmas_count()
    karmas_count = _karmas["karmas_count"]
    karmas_chats_count = _karmas["chats_count"]

    # Contributors/Developers count and commits on github
    url = "https://api.github.com/repos/thehamkercat/williambutcherbot/contributors"
    rurl = "https://github.com/thehamkercat/williambutcherbot"
    developers = await fetch(url)
    commits = 0
    for developer in developers:
        commits += developer['contributions']
    developers = len(developers)

    msg = f"""

**Global Stats of {BOT_NAME}**:
**{gbans}** Globally banned users.
**{total_users}** Users, Across **{len(served_chats)}** chats.
**{filters_count}** Filters, Across **{filters_chats_count}** chats.
**{notes_count}** Notes, Across **{notes_chats_count}** chats.
**{warns_count}** Warns, Across **{warns_chats_count}** chats.
**{karmas_count}** Karma, Across **{karmas_chats_count}** chats.
**{developers}** Developers And **{commits}** Commits On **[Github]({rurl})**."""

    await m.edit(msg, disable_web_page_preview=True)
