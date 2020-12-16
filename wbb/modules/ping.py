from wbb import app
import time
from wbb.utils import cust_filter
import requests
import inspect
__MODULE__ = "Ping"
__HELP__ = " - /ping - to check if I am Alive or Not"



@app.on_message(cust_filter.command(commands=(["ping"])))
async def ping(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("```Wait, Pinging all Datacenters```")
    result = ""
    for i in range(1, 6):
        dc = (f"https://cdn{i}.telesco.pe")
        ping1 = round(requests.head(dc).elapsed.total_seconds() * 1000)   
        result += f'```DC{i} - {ping1}ms```'
    await m.edit(result)
