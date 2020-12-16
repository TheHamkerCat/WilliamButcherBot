from wbb import app
import time
from wbb.utils import cust_filter
import requests
__MODULE__ = "Ping"
__HELP__ = " - /ping - to check if I am Alive or Not"


@app.on_message(cust_filter.command(commands=(["ping"])))
async def ping(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("Wait, Pinging all Datacenters")
    ping1 = round(requests.head("https://cdn1.telesco.pe/").elapsed.total_seconds() * 1000)
    ping2 = round(requests.head("https://cdn2.telesco.pe/").elapsed.total_seconds() * 1000)
    ping3 = round(requests.head("https://cdn3.telesco.pe/").elapsed.total_seconds() * 1000)
    ping4 = round(requests.head("https://cdn4.telesco.pe/").elapsed.total_seconds() * 1000)
    ping5 = round(requests.head("https://cdn5.telesco.pe/").elapsed.total_seconds() * 1000)
    await m.edit(f'''
```DC1 - {ping1}ms
DC2 - {ping2}ms
DC3 - {ping3}ms
DC4 - {ping4}ms
DC5 - {ping5}ms```
''')