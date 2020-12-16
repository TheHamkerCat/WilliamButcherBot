from wbb import app
import time
from wbb.utils import cust_filter

__MODULE__ = "Ping"
__HELP__ = " - /ping - to check if I am Alive or Not"


@app.on_message(cust_filter.command(commands=(["ping"])))
async def ping(client, message):
    start_time = int(round(time.time() * 1000))
    m = await message.reply_text("Starting Ping")
    end_time = int(round(time.time() * 1000))
    await m.edit(f"{end_time - start_time} ms")
