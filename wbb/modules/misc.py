from wbb import app
from wbb.utils import cust_filter, random_line

__MODULE__ = "Misc"
__HELP__ = '''
/commit - Generate Funny Commit Messages
/runs - Idk Test Yourself
/quote - Get Random Linux Quotes'''


@app.on_message(cust_filter.command(commands=("commit")))
async def commit(client, message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(cust_filter.command(commands=("runs")))
async def commit(client, message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))

@app.on_message(cust_filter.command(commands=("quote")))
async def quotes(client, message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))