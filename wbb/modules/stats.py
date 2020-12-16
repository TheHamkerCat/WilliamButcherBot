from wbb import app
from pyrogram import filters
import psutil
from wbb.utils import cust_filter

__MODULE__ = "Stats"
__HELP__ = "For Bot Owner to Check system Status"

@app.on_message(cust_filter.command(commands=(["stats"])))
async def stats(client, message):
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>CPU:</b> {cpu}% ' \
            f'<b>RAM:</b> {mem}% ' \
            f'<b>Disk:</b> {disk}%'
    await message.reply_text(stats)