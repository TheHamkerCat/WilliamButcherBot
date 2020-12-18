from wbb.utils import cust_filter, nekobin, formatter
from wbb import app, OWNER_ID, SUDO_USER_ID, bot_start_time, NEOFETCH
from pyrogram import filters, types
import re
import speedtest
import psutil
import time
import os


__MODULE__ = "Sudoers"
__HELP__ = '''
/log - To Get Logs From Last Run.
/speedtest - To Perform A Speedtest.
/stats - To Check System Status.
'''

SUDOERS = [OWNER_ID, SUDO_USER_ID]


# Logs Module


@app.on_message(filters.user(SUDOERS) & cust_filter.command("log"))
async def logs_chat(client, message):
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
        f = open("error.log", "r")
        data = await nekobin.neko(f.read())
        keyb = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Pasted!", url=f"{data}")]]
        )
        await query.message.edit_caption(
                                            "Successfully Nekofied",
                                            reply_markup=keyb
                                        )
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
    filters.user(SUDOERS) & cust_filter.command(commands=("speedtest"))
)
async def speeeed(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("```Performing A Speedtest!```")
    speed = speedtest.Speedtest()
    x = speed.get_best_server()
    y = speed.download()
    z = speed.upload()
    await m.edit(f'''
```Download - {speed_convert(y)}
Upload   - {speed_convert(z)}
Latency  - {round((x["latency"]))} ms
```''')

# Stats Module


@ app.on_message(
    filters.user(SUDOERS) & cust_filter.command(commands=("stats"))
)
async def stats(client, message):
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    if NEOFETCH == "True":
        os.system("neofetch --stdout > neofetch.txt")
        f = open("neofetch.txt", "r")
        read_file = f.read()
        neofetch = (f'''
----------[Neofetch]----------

{read_file}
''')
        f.close()
    else:
        neofetch = "NeoFetch Is Disabled!"
    stats = (f'''
```
----------[Stats]----------

      Uptime: {formatter.get_readable_time((bot_uptime))}
      CPU: {cpu}%
      RAM: {mem}%
      Disk: {disk}%

{neofetch}
```''')
    await message.reply_text(stats)
