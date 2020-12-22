import requests
from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter

__MODULE__ = "Ping"
__HELP__ = " /ping - To Get Response Time From All TG Datacenters"


@app.on_message(cust_filter.command(commands=("ping")))
async def ping(client, message: Message):  # pylint: disable=W0613
    app.set_parse_mode("markdown")
    j = await message.reply_text("Wait, Pinging all Datacenters`")
    result = ""
    for i in range(1, 6):
        datacenter = (f"https://cdn{i}.telesco.pe")
        ping1 = round(requests.head(datacenter).elapsed.total_seconds() * 1000)
        result += f'```DC{i} - {ping1}ms```'
    await j.edit(result)
