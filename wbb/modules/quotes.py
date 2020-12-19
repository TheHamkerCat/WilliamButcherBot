from wbb import app
from wbb.utils import cust_filter, random_line

__MODULE__ = "Quotes"
__HELP__ = "/quote - Generate Funny Linux Quotes"


@app.on_message(cust_filter.command(commands=("quote")))
async def quotes(client, message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))
