import secrets
import string
import requests
from pyrogram import filters
from pyrogram.types import Message
from googletrans import Translator
from cryptography.fernet import Fernet
from wbb import app, FERNET_ENCRYPTION_KEY
from wbb.utils import cust_filter, random_line
from wbb.utils.errors import capture_err

__MODULE__ = "Misc"
__HELP__ = '''/commit - Generate Funny Commit Messages
/runs  - Idk Test Yourself
/quote - Get Random Linux Quotes
/id - Get Chat_ID or User_ID
/random - Generate Random Complex Passwords
/http - Get Cats Reference Photo For Http Error Codes
/encrypt - Encrypt Text [Can Only Be Decrypted By This Bot]
/decrypt - Decrypt Text
/ipinfo - Get Info About An Ip Address
/cheat - Get Programming Related Help
/weather - To Get Weather Info
/tr - Translate A Message
#RTFM - Check it lol'''


@app.on_message(cust_filter.command(commands=("commit")) & ~filters.edited)
@capture_err
async def commit(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))

@app.on_message(filters.command("RTFM", "#"))
@capture_err
async def rtfm(_, message):
    await message.delete()
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message lol")
        return
    await message.reply_to_message.reply_text("Are You Lost? READ THE FUCKING DOCS!")


@app.on_message(cust_filter.command(commands=("runs")) & ~filters.edited)
@capture_err
async def runs(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(cust_filter.command(commands=("id")) & ~filters.edited)
@capture_err
async def get_id(_, message: Message):
    if len(message.command) != 1:
        username = message.text.split(None, 1)[1]
        user_id = (await app.get_users(username)).id
        msg = f"{username}'s ID is `{user_id}`"
        await message.reply_text(msg)

    elif len(message.command) == 1 and not message.reply_to_message:
        chat_id = message.chat.id
        msg = f"{message.chat.title}'s ID is `{chat_id}`"
        await message.reply_text(msg)

    elif len(message.command) == 1 and message.reply_to_message:
        from_user_id = message.reply_to_message.from_user.id
        from_user_mention = message.reply_to_message.from_user.mention
        msg = f"{from_user_mention}'s ID is `{from_user_id}`"
        await message.reply_text(msg)

# Random


@app.on_message(cust_filter.command(commands=('random')) & ~filters.edited)
@capture_err
async def random(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text('"/random" Needs An Argurment.'
                                 ' Ex: `/random 5`')
        random
    length = message.text.split(None, 1)[1]

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

# Encrypt


@app.on_message(cust_filter.command(commands=('encrypt')) & ~filters.edited)
@capture_err
async def encrypt(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Encrypt It.')
        return
    text = message.reply_to_message.text
    text_in_bytes = bytes(text, 'utf-8')
    cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
    encrypted_text = cipher_suite.encrypt(text_in_bytes)
    bytes_in_text = encrypted_text.decode("utf-8")
    await message.reply_text(bytes_in_text)

# Decrypt


@app.on_message(cust_filter.command(commands=('decrypt')) & ~filters.edited)
@capture_err
async def decrypt(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Decrypt It.')
        return
    text = message.reply_to_message.text
    text_in_bytes = bytes(text, 'utf-8')
    cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
    decoded_text = cipher_suite.decrypt(text_in_bytes)
    bytes_in_text = decoded_text.decode("utf-8")
    await message.reply_text(bytes_in_text)


# Cheat.sh


@app.on_message(cust_filter.command(commands=("cheat")) & ~filters.edited)
@capture_err
async def cheat(_, message: Message):
    text = message.text.split(None, 1)[1]
    ftext = text.split()
    try:
        language = ftext[0]
    except IndexError:
        await message.reply_text("/cheat [language] [query]")
        return
    try:
        query = ftext[1]
    except IndexError:
        await message.reply_text("/cheat [language] [query]")
        return
    r = requests.get(f"http://cht.sh/{language}/{query}?QT")
    reply = r.text
    await message.reply_text(f"`{reply}`")

# Weather


@app.on_message(cust_filter.command(commands=("weather")) & ~filters.edited)
@capture_err
async def weather(_, message: Message):
    city = message.text.split(None, 1)[1]
    if len(message.command) != 2:
        await message.reply_text("/weather [city]")
        return
    r = requests.get(f"https://wttr.in/{city}?mnTC0")
    data = r.text
    await message.reply_text(f"`{data}`")

# Translate


@app.on_message(cust_filter.command(commands=("tr")) & ~filters.edited)
@capture_err
async def tr(_, message: Message):
    lang = message.text.split(None, 1)[1]
    if not message.reply_to_message or lang == "":
        await message.reply_text(
            "Reply to a message with /tr [language code]"
            + "\nGet supported language list from here -"
            + " https://py-googletrans.readthedocs.io/en"
            + "/latest/#googletrans-languages"
        )
        return
    text = message.reply_to_message.text
    i = Translator().translate(text, dest=lang)
    await message.reply_text(i.text)


@app.on_message(filters.command('bun'))
@capture_err
async def bunn(_, message):
    if message.reply_to_message:
        await message.reply_to_message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")
        return
    if not message.reply_to_message:
        await message.reply_sticker('CAACAgUAAx0CWIlO9AABARyRYBhyjKXFATVhu7AGQwip3TzSFiMAAuMBAAJ7usBUIu2xBtXTmuweBA')
        await app.send_message(message.chat.id, text="Eat Bun")
