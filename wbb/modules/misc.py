import secrets
import string
import requests
import ipinfo
from pyrogram import filters
from pyrogram.types import Message
from cryptography.fernet import Fernet
from wbb.utils.botinfo import BOT_ID
from wbb import app, FERNET_ENCRYPTION_KEY
from wbb.utils import cust_filter, random_line

__MODULE__ = "Misc"
__HELP__ = '''/commit - Generate Funny Commit Messages
/runs  - Idk Test Yourself
/quote - Get Random Linux Quotes
/id - Get Chat_ID or User_ID
/dev - Forward Anything To Developers [SPAM = GBAN]
/random - Generate Random Complex Passwords
/http - Get Cats Reference Photo For Http Error Codes
/encrypt - Encrypt Text [Can Only Be Decrypted By This Bot]
/decrypt - Decrypt Text
/ipinfo - Get Info About An Ip Address
/cheat - Get Programming Related Help'''


@app.on_message(cust_filter.command(commands=("commit")) & ~filters.edited)
async def commit(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/commit.txt')))


@app.on_message(cust_filter.command(commands=("runs")) & ~filters.edited)
async def runs(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/runs.txt')))


@app.on_message(cust_filter.command(commands=("quote")) & ~filters.edited)
async def quote(_, message: Message):
    await message.reply_text((await random_line('wbb/utils/quotes.txt')))


@app.on_message(cust_filter.command(commands=("id")) & ~filters.edited)
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


@app.on_message(cust_filter.command(commands=("dev")) & ~filters.edited)
async def dev(_, message: Message):
    app.set_parse_mode("markdown")
    if (await app.get_chat_member(
            message.chat.id,
            BOT_ID)).can_restrict_members:

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
    else:
        await message.reply_text("To Use This Feature You Have To Make Me"
                                 + " Admin")
# Password


@app.on_message(cust_filter.command(commands=('random')) & ~filters.edited)
async def random(_, message: Message):
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
        await message.reply_text('"/random" Needs An Argurment.'
                                 ' Ex: `/random 5`')

# http cat search


@app.on_message(cust_filter.command(commands=('http')) & ~filters.edited)
async def http(_, message: Message):
    if message.text != "/http":
        code = message.text.replace('/http', '')
        url = f"https://http.cat/{code}"
        final = url.replace(' ', '')
        await message.reply_photo(final)
    else:
        await message.reply_text('"/http" Needs An Argument. Ex: `/http 404`')


# Encrypt


@app.on_message(cust_filter.command(commands=('encrypt')) & ~filters.edited)
async def encrypt(_, message: Message):
    app.set_parse_mode('markdown')
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Encrypt It.')
    else:
        text = message.reply_to_message.text
        text_in_bytes = bytes(text, 'utf-8')
        cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
        encrypted_text = cipher_suite.encrypt(text_in_bytes)
        bytes_in_text = encrypted_text.decode("utf-8")
        await message.reply_text(bytes_in_text)

# Decrypt


@app.on_message(cust_filter.command(commands=('decrypt')) & ~filters.edited)
async def decrypt(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text('Reply To A Message To Decrypt It.')
    else:
        text = message.reply_to_message.text
        text_in_bytes = bytes(text, 'utf-8')
        cipher_suite = Fernet(FERNET_ENCRYPTION_KEY)
        decoded_text = cipher_suite.decrypt(text_in_bytes)
        bytes_in_text = decoded_text.decode("utf-8")
        await message.reply_text(bytes_in_text)

# Ipinfo


@app.on_message(cust_filter.command(commands=('ipinfo')) & ~filters.edited)
async def ipaddrinfo(_, message: Message):
    app.set_parse_mode('markdown')
    ipaddr = message.text.replace("/ipinfo", "")
    if ipaddr != "":
        handler = ipinfo.getHandler()
        details = handler.getDetails(ipaddr)
        await message.reply_text(f'''`IP - {details.ip}
City - {details.city}
Region - {details.region}
Country - {details.country}
Location - {details.loc}
ORG - {details.org}
Postal - {details.postal}
Timezone - {details.timezone}`''')

    else:
        await message.reply_text('`/ipinfo` Requires An IP As Argument'
                                 + '. Ex - `/ipinfo 1.1.1.1`')


@app.on_message(cust_filter.command(commands=("cheat")) & ~filters.edited)
async def cheat(_, message: Message):
    text = message.text.replace("/cheat ", "")
    ftext = text.split()
    try:
        language = ftext[0]
    except IndexError:
        await message.reply_text("/cheat [language] [query]")
    try:
        query = ftext[1]
    except IndexError:
        await message.reply_text("/cheat [language] [query]")
    r = requests.get(f"http://cht.sh/{language}/{query}?QT")
    reply = r.text
    await message.reply_text(f"`{reply}`")
