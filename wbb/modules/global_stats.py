"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait

from wbb import BOT_ID, BOT_NAME, SUDOERS, USERBOT_NAME, app, app2
from wbb.core.decorators.errors import capture_err
from wbb.modules import ALL_MODULES
from wbb.utils.dbfunctions import (get_blacklist_filters_count,
                                   get_filters_count, get_gbans_count,
                                   get_karmas_count, get_notes_count,
                                   get_rss_feeds_count, get_served_chats,
                                   get_served_users, get_warns_count,
                                   remove_served_chat)
from wbb.utils.http import get
from wbb.utils.inlinefuncs import keywords_list


@app.on_message(
    filters.command("clean_db") & filters.user(SUDOERS) & ~filters.edited
)
@capture_err
async def clean_db(_, message):
    served_chats = [int(i["chat_id"]) for i in (await get_served_chats())]
    m = await message.reply(
        f"__**Cleaning database, Might take around {len(served_chats)*2} seconds.**__",
    )
    for served_chat in served_chats:
        try:
            await app.get_chat_members(served_chat, BOT_ID)
            await asyncio.sleep(2)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            await remove_served_chat(served_chat)
            served_chats.remove(served_chat)
            pass
    await m.edit("**Database Cleaned.**")


@app.on_message(
    filters.command("gstats") & filters.user(SUDOERS) & ~filters.edited
)
@capture_err
async def global_stats(_, message):
    m = await app.send_message(
        message.chat.id,
        text="__**Analysing Stats...**__",
        disable_web_page_preview=True,
    )

    # For bot served chat and users count
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    # Gbans count
    gbans = await get_gbans_count()
    _notes = await get_notes_count()
    notes_count = _notes["notes_count"]
    notes_chats_count = _notes["chats_count"]

    # Filters count across chats
    _filters = await get_filters_count()
    filters_count = _filters["filters_count"]
    filters_chats_count = _filters["chats_count"]

    # Blacklisted filters count across chats
    _filters = await get_blacklist_filters_count()
    blacklist_filters_count = _filters["filters_count"]
    blacklist_filters_chats_count = _filters["chats_count"]

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
    developers = await get(url)
    commits = 0
    for developer in developers:
        commits += developer["contributions"]
    developers = len(developers)

    # Rss feeds
    rss_count = await get_rss_feeds_count()
    # Modules info
    modules_count = len(ALL_MODULES)

    # Userbot info
    groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
    async for i in app2.iter_dialogs():
        t = i.chat.type
        total_ub += 1

        if t in ["supergroup", "group"]:
            groups_ub += 1
        elif t == "channel":
            channels_ub += 1
        elif t == "bot":
            bots_ub += 1
        elif t == "private":
            privates_ub += 1

    msg = f"""
**Global Stats of {BOT_NAME}**:
    **{modules_count}** Modules Loaded.
    **{len(keywords_list)}** Inline Modules Loaded.
    **{rss_count}** Active RSS Feeds.
    **{gbans}** Globally banned users.
    **{filters_count}** Filters, Across **{filters_chats_count}** chats.
    **{blacklist_filters_count}** Blacklist Filters, Across **{blacklist_filters_chats_count}** chats.
    **{notes_count}** Notes, Across **{notes_chats_count}** chats.
    **{warns_count}** Warns, Across **{warns_chats_count}** chats.
    **{karmas_count}** Karma, Across **{karmas_chats_count}** chats.
    **{served_users}** Users, Across **{served_chats}** chats.
    **{developers}** Developers And **{commits}** Commits On **[Github]({rurl})**.

**Global Stats of {USERBOT_NAME}**:
    **{total_ub} Dialogs.**
    **{groups_ub} Groups Joined.**
    **{channels_ub} Channels Joined.**
    **{bots_ub} Bots.**
    **{privates_ub} Users.**
"""
    await m.edit(msg, disable_web_page_preview=True)
