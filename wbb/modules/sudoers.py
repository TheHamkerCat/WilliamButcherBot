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
import os
import subprocess
import time

import psutil
from pyrogram import filters

from wbb import (BOT_ID, GBAN_LOG_GROUP_ID, SUDOERS, USERBOT_USERNAME, app,
                 bot_start_time)
from wbb.core.decorators.errors import capture_err
from wbb.utils import formatter
from wbb.utils.dbfunctions import (add_gban_user, get_served_chats,
                                   is_gbanned_user, remove_gban_user,
                                   start_restart_stage)

__MODULE__ = "Sudoers"
__HELP__ = """
/stats - To Check System Status.
/gstats - To Check Bot's Global Stats.
/gban - To Ban A User Globally.
/broadcast - To Broadcast A Message To All Groups.
/update - To Update And Restart The Bot
"""

# Stats Module


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
{USERBOT_USERNAME}@William
------------------
UPTIME: {formatter.get_readable_time((bot_uptime))}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""
    return stats


@app.on_message(filters.user(SUDOERS) & filters.command("stats"))
@capture_err
async def get_stats(_, message):
    stats = await bot_sys_stats()
    await message.reply_text(stats)


# Gban


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
@capture_err
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 3:
            return await message.reply_text(
                "**Usage:**\n/gban [USERNAME | USER_ID] [REASON]"
            )
        user = message.text.split(None, 2)[1]
        reason = message.text.split(None, 2)[2]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            await message.reply_text("You want to gban yourself? FOOL!")
        elif user.id == BOT_ID:
            await message.reply_text(
                "Should i gban myself? I'm not fool like you, HUMAN!"
            )
        elif user.id in SUDOERS:
            await message.reply_text("You want to ban a sudo user? GET REKT!!")
        else:
            served_chats = await get_served_chats()
            m = await message.reply_text(
                f"**Initializing WBB Global Ban Sequence To Add Restrictions On {user.mention}**"
                + f" **This Action Should Take About {len(served_chats)} Seconds.**"
            )
            await add_gban_user(user.id)
            number_of_chats = 0
            for served_chat in served_chats:
                try:
                    await app.kick_chat_member(served_chat["chat_id"], user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except Exception:
                    pass
            try:
                await app.send_message(
                    user.id,
                    f"Hello, You have been globally banned by {from_user.mention},"
                    + " You can appeal for this ban in @WBBSupport.",
                )
            except Exception:
                pass
            await m.edit(f"Banned {user.mention} Globally!")
            ban_text = f"""
__**New Global Ban**__
**Origin:** {message.chat.title} [`{message.chat.id}`]
**Admin:** {from_user.mention}
**Banned User:** {user.mention}
**Banned User ID:** `{user.id}`
**Reason:** __{reason}__
**Chats:** `{number_of_chats}`"""
            try:
                m2 = await app.send_message(
                    GBAN_LOG_GROUP_ID,
                    text=ban_text,
                    disable_web_page_preview=True,
                )
                await m.edit(
                    f"Banned {user.mention} Globally!\nAction Log: {m2.link}",
                    disable_web_page_preview=True,
                )
            except Exception:
                await message.reply_text(
                    "User Gbanned, But This Gban Wasn't Logged, Add Bot In GBAN_LOG_GROUP"
                )
                return
        return
    if len(message.command) < 2:
        await message.reply_text("**Usage:**\n/gban [REASON]")
        return
    reason = message.text.strip().split(None, 1)[1]
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("You want to gban yourself? FOOL!")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Should i gban myself? I'm not fool like you, HUMAN!"
        )
    elif user_id in SUDOERS:
        await message.reply_text("You want to ban a sudo user? GET REKT!!")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("He's already gbanned, why bully him?")
        else:
            served_chats = await get_served_chats()
            m = await message.reply_text(
                f"**Initializing WBB Global Ban Sequence To Add Restrictions On {mention}**"
                + f" **This Action Should Take About {len(served_chats)} Seconds.**"
            )
            number_of_chats = 0
            for served_chat in served_chats:
                try:
                    await app.kick_chat_member(served_chat["chat_id"], user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except Exception:
                    pass
            await add_gban_user(user_id)
            try:
                await app.send_message(
                    user_id,
                    f"""
Hello, You have been globally banned by {from_user_mention},
You can appeal for this ban in @WBBSupport.""",
                )
            except Exception:
                pass
            await m.edit(f"Banned {mention} Globally!")
            ban_text = f"""
__**New Global Ban**__
**Origin:** {message.chat.title} [`{message.chat.id}`]
**Admin:** {from_user_mention}
**Banned User:** {mention}
**Banned User ID:** `{user_id}`
**Reason:** __{reason}__
**Chats:** `{number_of_chats}`"""
            try:
                m2 = await app.send_message(
                    GBAN_LOG_GROUP_ID,
                    text=ban_text,
                    disable_web_page_preview=True,
                )
                await m.edit(
                    f"Banned {mention} Globally!\nAction Log: {m2.link}",
                    disable_web_page_preview=True,
                )
            except Exception:
                await message.reply_text(
                    "User Gbanned, But This Gban Wasn't Logged, Add Bot In GBAN_LOG_GROUP"
                )


# Ungban


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
@capture_err
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "Reply to a user's message or give username/user_id."
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            await message.reply_text("You want to ungban yourself? FOOL!")
        elif user.id == BOT_ID:
            await message.reply_text(
                "Should i ungban myself? But i'm not gbanned."
            )
        elif user.id in SUDOERS:
            await message.reply_text("Sudo users can't be gbanned/ungbanned.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("He's already free, why bully him?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Unbanned {user.mention} Globally!")
        return

    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("You want to ungban yourself? FOOL!")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Should i ungban myself? But i'm not gbanned."
        )
    elif user_id in SUDOERS:
        await message.reply_text("Sudo users can't be gbanned/ungbanned.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("He's already free, why bully him?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Unbanned {mention} Globally!")


# Broadcast


@app.on_message(
    filters.command("broadcast") & filters.user(SUDOERS) & ~filters.edited
)
@capture_err
async def broadcast_message(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage**:\n/broadcast [MESSAGE]")
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            await app.send_message(i, text=text)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**Broadcasted Message In {sent} Chats.**")


# Update


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_restart(_, message):
    await message.reply_text(
        f'```{subprocess.check_output(["git", "pull"]).decode("UTF-8")}```'
    )
    m = await message.reply_text(
        "**Updated with default branch, restarting now**"
    )
    await start_restart_stage(m.chat.id, m.message_id)
    os.execvp("python3", ["python3", "-m", "wbb"])
