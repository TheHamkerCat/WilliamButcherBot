from wbb import app
from wbb.utils import cust_filter, random_line
from pyrogram.types import Message

__MODULE__ = "Misc"
__HELP__ = "/commit - Generate Funny Commit Messages\n" \
           "/runs - Idk Test Yourself\n" \
           "/quote - Get Random Linux Quotes\n" \
           "/id - Get Chat_ID or User_ID\n" \
           "/dev - Forward Anything To Developers [SPAM = GBAN]"


@app.on_message(cust_filter.command(commands=("commit")))
async def commit(client, message: Message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(cust_filter.command(commands=("runs")))
async def runs(client, message: Message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(cust_filter.command(commands=("quote")))
async def quote(client, message: Message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))


@app.on_message(cust_filter.command(commands=("id")))
async def id(client, message: Message):
    app.set_parse_mode("markdown")
    if message.text != '/id':
        username = message.text.replace('/id', '')
        id = (await app.get_users(username)).id
        msg = f"{username}'s ID is `{id}`"
        await message.reply_text(msg)

    elif message.text == '/id' and not bool(message.reply_to_message):
        id = message.chat.id
        msg = f"{message.chat.title}'s ID is `{id}`"
        await message.reply_text(msg)

    elif message.text == '/id' and bool(message.reply_to_message):
        id = message.reply_to_message.from_user.id
        msg = f"{message.reply_to_message.from_user.mention}'s ID is `{id}`"
        await message.reply_text(msg)


@app.on_message(cust_filter.command(commands=("dev")))
async def dev(client, message: Message):
    app.set_parse_mode("markdown")
    await message.reply_to_message.forward('WBBSupport')
    await app.send_message("WBBSupport",
                           f"Forwarded By ID: `{message.from_user.id}`")
    await message.reply_text("Your Message Has Been Forward To Devs,"
                             + " Any Missuse Of This Feature Will Not"
                             + " Be Tolerated And You Will Be"
                             + " Gbanned instantaneously!")
