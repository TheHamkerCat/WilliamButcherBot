import re
import time
from pyrogram import filters, types
import speedtest
import psutil
from wbb.utils import nekobin, formatter
from wbb.utils.errors import capture_err
from wbb import app, SUDOERS, bot_start_time

__MODULE__ = "Sudoers"
__HELP__ = '''/log - To Get Logs From Last Run.
/speedtest - To Perform A Speedtest.
/stats - To Check System Status.
/song - To Download Songs From JioSaavn'''


# Logs Module


@app.on_message(filters.user(SUDOERS) & filters.command("log"))
@capture_err
async def logs_chat(_, message):
    keyb = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Paste on Nekobin", callback_data="paste_log_nekobin"
                )
            ]
        ]
    )
    await message.reply_document(
        "error.log", reply_markup=keyb
    )


def logs_callback(_, __, query):
    if re.match("paste_log_nekobin", query.data):
        return True


logs_create = filters.create(logs_callback)


@app.on_callback_query(logs_create)
async def paste_log_neko(client, query):
    if query.from_user.id == OWNER_ID or SUDO_USER_ID:
        j = open("error.log", "r")
        data = await nekobin.neko(j.read())
        keyb = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Pasted!", url=f"{data}")]]
        )
        await query.message.edit_caption("Successfully Nekofied",
                                         reply_markup=keyb)
    else:
        await client.answer_callback_query(
            query.id, "'Blue Button Must Press', huh?", show_alert=True
        )


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
```Download - {speed_convert(j)}
Upload   - {speed_convert(k)}
Latency  - {round((i["latency"]))} ms
```''')

# Stats Module


@app.on_message(
    filters.user(SUDOERS) & filters.command("stats")
)
@capture_err
async def get_stats(_, message):
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (f'''```Uptime: {formatter.get_readable_time((bot_uptime))}
CPU: {cpu}%
RAM: {mem}%
Disk: {disk}%```''')
    await message.reply_text(stats)
