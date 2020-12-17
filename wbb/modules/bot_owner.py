from wbb.utils import cust_filter, nekobin, formater
from wbb import app, Command, OWNER_ID, bot_start_time
from pyrogram import filters, types
import re, speedtest, psutil, time, os


__MODULE__ = "BotOwner"
__HELP__ = '''
/log - To Get Logs From Last Run.
/speedtest - To Perform A Speedtest.
/stats - For Bot Owner To Check System Status.

'''

#Logs Module

@app.on_message(filters.user(OWNER_ID) & cust_filter.command("log"))
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
        "error.log", caption="**Here are my Logs ~**", reply_markup=keyb
    )


def logs_callback(_, __, query):
    if re.match("paste_log_nekobin", query.data):
        return True


logs_create = filters.create(logs_callback)


@app.on_callback_query(logs_create)
async def paste_log_neko(client, query):
    if query.from_user.id == OWNER_ID:
        f = open("error.log", "r")
        data = await nekobin.neko(f.read())
        keyb = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("pasted on nekobin", url=f"{data}")]]
        )
        await query.message.edit_caption("Successfully Nekofied", reply_markup=keyb)
    else:
        await client.answer_callback_query(
            query.id, "'Blue Button Must Press', huh?", show_alert=True
        )



#SpeedTest Module

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


#Stats Module

@app.on_message(filters.user(OWNER_ID) & cust_filter.command(commands=(["stats"])))
async def stats(client, message):
    neofetch = os.system("neofetch --stdout")
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (f'''
```#####-Stats-#####
Uptime: {formater.get_readable_time((time.time() - bot_start_time))} 
CPU: {cpu}% 
RAM: {mem}% 
Disk: {disk}%

####-Neofetch-####
{neofetch}
```''')
    await message.reply_text(stats)

