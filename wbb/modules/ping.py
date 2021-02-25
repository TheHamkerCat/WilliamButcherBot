import requests
from pyrogram import filters
from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter
from wbb.utils.botinfo import BOT_DC_ID
from wbb.utils.errors import capture_err

__MODULE__ = "Ping"
__HELP__ = " /ping - To Get Response Time From All TG Datacenters"


@app.on_message(cust_filter.command(commands=("ping")) & ~filters.edited)
@capture_err
async def ping(_, message: Message):
    datacenter = (f"https://cdn{BOT_DC_ID}.telesco.pe")
    ping1 = round(requests.head(datacenter).elapsed.total_seconds() * 1000)
    result = f'`DC{BOT_DC_ID} - {ping1}ms`\n'
    await message.reply_text(result)
