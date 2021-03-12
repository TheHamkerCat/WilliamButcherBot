import requests
from pyrogram import filters
from wbb import app
from wbb.utils.botinfo import BOT_DC_ID
from wbb.utils.errors import capture_err

__MODULE__ = "Ping"
__HELP__ = " /ping - To Get Response Time From All TG Datacenters"


@app.on_message(filters.command("ping") & ~filters.edited)
@capture_err
async def ping(_, message):
    datacenter = (f"https://cdn{BOT_DC_ID}.telesco.pe")
    ping1 = round(requests.head(datacenter).elapsed.total_seconds() * 1000)
    result = f'`DC{BOT_DC_ID} - {ping1}ms`\n'
    await message.reply_text(result)
