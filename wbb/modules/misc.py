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
from wbb.utils.json_prettify import json_prettify
from wbb.utils.fetch import fetch
from wbb.utils.nekobin import neko


__MODULE__ = "Misc"
__HELP__ = '''/commit - Generate Funny Commit Messages
/runs  - Idk Test Yourself
/id - Get Chat_ID or User_ID
/random - Generate Random Complex Passwords
/encrypt - Encrypt Text [Can Only Be Decrypted By This Bot]
/decrypt - Decrypt Text
/cheat - Get Programming Related Help
/weather - To Get Weather Info
/tr [en] - Translate A Message
/json [URL] - Get Response From An API or Something. 
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
        return
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
    if len(message.command) < 3:
        await message.reply_text("/cheat [language] [query]")
        return
    text = message.text.split(None, 1)[1]
    m = await message.reply_text("Searching")
    try:
        ftext = text.split()
        language = ftext[0]
        query = ftext[1]
        data = requests.get(f"http://cht.sh/{language}/{query}?QT").text
        if not data:
            await m.edit("Found Literally Nothing!")
            return
        await m.edit(f"`{data}`")
    except Exception as e:
        await m.edit(str(e))
        print(str(e))

# Weather


@app.on_message(cust_filter.command(commands=("weather")) & ~filters.edited)
@capture_err
async def weather(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("/weather [city]")
        return
    city = message.text.split(None, 1)[1]
    m = await message.reply_text("Fetching Data")
    r = requests.get(f"https://wttr.in/{city}?mnTC0")
    data = r.text
    await m.edit(f"`{data}`")

# Translate


@app.on_message(cust_filter.command(commands=("tr")) & ~filters.edited)
@capture_err
async def tr(_, message):
    if len(message.command) != 2:
        await message.reply_text("/tr [LANGUAGE_CODE]")
        return
    lang = message.text.split(None, 1)[1]
    if not message.reply_to_message or not lang:
        await message.reply_text(
            "Reply to a message with /tr [language code]"
            + "\nGet supported language list from here -"
            + " https://py-googletrans.readthedocs.io/en"
            + "/latest/#googletrans-languages"
        )
        return
    if message.reply_to_message.text:
        text = message.reply_to_message.text
        i = Translator().translate(text, dest=lang)
        await message.reply_text(i.text)
    elif message.reply_to_message.caption:
        text = message.reply_to_message.caption
        i = Translator().translate(text, dest=lang)
        await message.reply_text(i.text)



fetch_limit = 0


@app.on_message(filters.command("json") & ~filters.edited)
@capture_err
async def json_fetch(_, message):
    global fetch_limit
    if len(message.command) != 2:
        await message.reply_text("/json [URL]")
        return
    elif fetch_limit > 500:
        await message.reply_text("Today's Quota Exceeded!, lol")
        return
    url = message.text.split(None, 1)[1]
    try:
        data = await fetch(url)
        data = await json_prettify(data)
        fetch_limit += 1
        if len(data) < 4090:
            await message.reply_text(data)
        else:
            neko_link = await neko(data)
            await message.reply_text(f"[OUTPUT_TOO_LONG]({neko_link})", disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))
    

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
