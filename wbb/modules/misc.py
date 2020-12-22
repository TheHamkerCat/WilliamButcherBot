import secrets
import string
from pyrogram.types import Message
from wbb import app
from wbb.utils import cust_filter, random_line

__MODULE__ = "Misc"
__HELP__ = "/commit - Generate Funny Commit Messages\n" \
           "/runs - Idk Test Yourself\n" \
           "/quote - Get Random Linux Quotes\n" \
           "/id - Get Chat_ID or User_ID\n" \
           "/dev - Forward Anything To Developers [SPAM = GBAN]"


@app.on_message(cust_filter.command(commands=("commit")))
async def commit(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(cust_filter.command(commands=("runs")))
async def runs(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(cust_filter.command(commands=("quote")))
async def quote(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))


@app.on_message(cust_filter.command(commands=("id")))
async def get_id(_, message: Message):
    app.set_parse_mode("markdown")
    if message.text != '/id':
        username = message.text.replace('/id', '')
        user_id = (await app.get_users(username)).id
        msg = f"{username}'s ID is `{user_id}`"
        await message.reply_text(msg)

    elif message.text == '/id' and not bool(message.reply_to_message):
        chat_id = message.chat.id
        msg = f"{message.chat.title}'s ID is `{chat_id}`"
        await message.reply_text(msg)

    elif message.text == '/id' and bool(message.reply_to_message):
        from_user_id = message.reply_to_message.from_user.id
        from_user_mention = message.reply_to_message.from_user.mention
        msg = f"{from_user_mention}'s ID is `{from_user_id}`"
        await message.reply_text(msg)


@app.on_message(cust_filter.command(commands=("dev")))
async def dev(_, message: Message):
    app.set_parse_mode("markdown")
    await message.reply_to_message.forward('WBBSupport')
    await app.send_message("WBBSupport",
                           "Forwarded By: `{}` | {}\n"
                           "Forwarded From: `{}` | {}"
                           .format(message.from_user.id,
                                   message.from_user.mention,
                                   message.chat.id,
                                   message.chat.title))
    await message.reply_text("Your Message Has Been Forward To Devs,"
                             + " Any Missuse Of This Feature Will Not"
                             + " Be Tolerated And You Will Be"
                             + " Gbanned instantaneously!")


# Password


@app.on_message(cust_filter.command(commands=('random')))
async def passwd(_, message: Message):
    app.set_parse_mode('markdown')
    if message.text != "/random":
        length = message.text.replace('/random', '')
        try:
            if 1 < int(length) < 1000:
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in
                                   range(int(length)))
                await message.reply_text(f"`{password}`")
            else:
                await message.reply_text('Specify A Length Between 1-1000')
        except ValueError:
            await message.reply_text("Strings Won't Work!, Pass A"
                                     + " Positive Integer Between 1-1000")
    else:
        await message.reply_text('"/random" Needs An Argurment')
