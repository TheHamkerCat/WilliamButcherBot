import time
import os
import subprocess
from pyrogram import filters
import speedtest
import psutil
import asyncio
from sys import version as pyver
from wbb import app, SUDOERS, bot_start_time, BOT_ID, USERBOT_USERNAME
from wbb.utils import formatter
from wbb.utils.errors import capture_err
from wbb.utils.dbfunctions import (
    is_gbanned_user,
    add_gban_user,
    remove_gban_user,
    get_served_chats
)


__MODULE__ = "Sudoers"
__HELP__ = '''/speedtest - To Perform A Speedtest.
/stats - To Check System Status.
/gstats - To Check Bot's Global Stats.
/gban - To Ban A User Globally.
/broadcast - To Broadcast A Message To All Groups.
/update - To Update And Restart The Bot'''


# SpeedTest Module


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@app.on_message(
    filters.user(SUDOERS) & filters.command("speedtest")
)
@capture_err
async def get_speedtest_result(_, message):
    m = await message.reply_text("`Performing A Speedtest!`")
    speed = speedtest.Speedtest()
    i = speed.get_best_server()
    j = speed.download()
    k = speed.upload()
    await m.edit(f'''
**Download:** `{speed_convert(j)}`
**Upload:** `{speed_convert(k)}`
**Latency:** `{round((i["latency"]))} ms`
''')

# Stats Module


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f'''
{USERBOT_USERNAME}@William
------------------
Uptime: {formatter.get_readable_time((bot_uptime))}
CPU: {cpu}%
RAM: {mem}%
Disk: {disk}%'''
    return stats


@app.on_message(
    filters.user(SUDOERS) & filters.command("stats")
)
@capture_err
async def get_stats(_, message):
    stats = await bot_sys_stats()
    await message.reply_text(stats)

# Gban


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
@capture_err
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("Reply to a user's message or give username/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user
        if user.id == from_user.id:
            await message.reply_text("You want to gban yourself? FOOL!")
        elif user.id == BOT_ID:
            await message.reply_text("Should i gban myself? I'm not fool like you, HUMAN!")
        elif user.id in SUDOERS:
            await message.reply_text("You want to ban a sudo user? GET REKT!!")
        else:
            served_chats = await get_served_chats()
            m = await message.reply_text(f"**{user.mention} Will Be Banned  Globally In {len(served_chats)} Seconds.**")
            await add_gban_user(user.id)
            for served_chat in served_chats:
                try:
                    await app.kick_chat_member(served_chat['chat_id'], user.id)
                    await asyncio.sleep(1)
                except Exception:
                    pass
            try:
                await app.send_message(
                    user.id, f"Hello, You have been globally banned by {from_user.mention},"
                    + " You can appeal for this ban by talking to {from_user.mention}.")
            except Exception:
                pass
            await m.edit(f"Banned {user.mention} Globally!")
        return

    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    from_user_mention = message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("You want to gban yourself? FOOL!")
    elif user_id == BOT_ID:
        await message.reply_text("Should i gban myself? I'm not fool like you, HUMAN!")
    elif user_id in SUDOERS:
        await message.reply_text("You want to ban a sudo user? GET REKT!!")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("He's already gbanned, why bully him?")
        else:
            served_chats = await get_served_chats()
            m = await message.reply_text(f"**{mention} Will Be Banned  Globally In {len(served_chats)} Seconds.**")
            for served_chat in served_chats:
                try:
                    await app.kick_chat_member(served_chat['chat_id'], user_id)
                    await asyncio.sleep(1)
                except Exception:
                    pass
            await add_gban_user(user_id)
            try:
                await app.send_message(
                    user_id, f"""
Hello, You have been globally banned by {from_user_mention},
You can appeal for this ban by talking to {from_user_mention}.""")
            except Exception:
                pass
            await m.edit(f"Banned {mention} Globally!")

# Ungban


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
@capture_err
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("Reply to a user's message or give username/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user
        if user.id == from_user.id:
            await message.reply_text("You want to ungban yourself? FOOL!")
        elif user.id == BOT_ID:
            await message.reply_text("Should i ungban myself? But i'm not gbanned.")
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
        await message.reply_text("Should i ungban myself? But i'm not gbanned.")
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
    filters.command("broadcast")
    & filters.user(SUDOERS)
    & ~filters.edited
)
@capture_err
async def broadcast_message(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage**:\n/broadcast [MESSAGE]")
        return
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
    await message.reply_text(f'```{subprocess.check_output(["git", "pull"]).decode("UTF-8")}```')
    os.execvp(f"python{str(pyver.split(' ')[0])[:3]}", [f"python{str(pyver.split(' ')[0])[:3]}", "-m", "wbb"])
