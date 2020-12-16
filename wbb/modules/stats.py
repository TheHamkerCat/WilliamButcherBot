from wbb import app, OWNER_ID, bot_start_time
import time
from pyrogram import filters
import psutil
from wbb.utils import cust_filter, formater

__MODULE__ = "Stats"
__HELP__ = "For Bot Owner to Check system Status"


@app.on_message(filters.user(OWNER_ID) & cust_filter.command(commands=(["stats"])))
async def stats(client, message):
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"<b>Uptime:</b> {formater.get_readable_time((time.time() - bot_start_time))}" f"\n<b>CPU:</b> {cpu}% " f"\n<b>RAM:</b> {mem}% " f"\n<b>Disk:</b> {disk}%"
    await message.reply_text(stats)
