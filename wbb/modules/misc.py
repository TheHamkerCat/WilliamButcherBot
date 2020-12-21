from wbb import app
from wbb.utils import cust_filter, random_line

__MODULE__ = "Misc"
__HELP__ = "/commit - Generate Funny Commit Messages\n" \
           "/runs - Idk Test Yourself\n" \
           "/quote - Get Random Linux Quotes\n" \
           "/id - Get Chat_ID or User_ID"


@app.on_message(cust_filter.command(commands=("commit")))
async def commit(client, message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(cust_filter.command(commands=("runs")))
async def runs(client, message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(cust_filter.command(commands=("quote")))
async def quote(client, message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))


@app.on_message(cust_filter.command(commands=("id")))
async def id(client, message):
    if message.text != '/id':
        username = message.text.replace('/id', '')
        id = (await app.get_users(username)).id
        msg = f"{username}'s ID is {id}"
        await message.reply_text(msg)

    elif message.text == '/id' and bool(message.reply_to_message) is False:
        id = message.chat.id
        msg = f"{message.chat.title}'s ID is {id}"
        await message.reply_text(msg)

    elif message.text == '/id' and bool(message.reply_to_message) is True:
        id = message.reply_to_message.from_user.id
        msg = f"{message.reply_to_message.from_user.first_name}'s ID is {id}"
        await message.reply_text(msg)
