from pyrogram import filters
from wbb import app, Command, OWNER_ID
from wbb.utils import cust_filter
import speedtest


__MODULE__ = "Speedtest"
__HELP__ = " - /speedtest - to perform a speedtest [only for owner]"


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@app.on_message(filters.user(OWNER_ID) & cust_filter.command(commands=(["speedtest"])))
async def speeeed(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("```Wait, Doing Speedtest!```")
    speed = speedtest.Speedtest()
    x = speed.get_best_server()
    y = speed.download()
    z = speed.upload()
    await m.edit(f'''
```Download - {speed_convert(y)}
Upload   - {speed_convert(z)}
Latency  - {round((x["latency"]))} ms
```''')
