"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from asyncio import get_event_loop
from inspect import getfullargspec
from os import environ
from time import ctime, time

from aiohttp import ClientSession
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph

load_dotenv("config.env")

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    print("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

API_ID = environ.get('API_ID', '')
if len(API_ID) == 0:
    print("API_ID variable is missing! Exiting now")
    exit(1)
else:
    API_ID = int(API_ID)

API_HASH = environ.get('API_HASH', '')
if len(API_HASH) == 0:
    print("API_HASH variable is missing! Exiting now")
    exit(1)

ARQ_API_KEY = environ.get('ARQ_API_KEY', '')
if len(ARQ_API_KEY) == 0:
    print("ARQ_API_KEY variable is missing! Exiting now\nGet this from @ARQRobot")
    exit(1)

MONGO_URL = environ.get('MONGO_URL', '')
if len(MONGO_URL) == 0:
    print("MONGO_URL variable is missing! Exiting now")
    exit(1)

MESSAGE_DUMP_CHAT = environ.get('MESSAGE_DUMP_CHAT', '')
if len(MESSAGE_DUMP_CHAT) == 0:
    print("MESSAGE_DUMP_CHAT variable is missing! Exiting now")
    exit(1)
else:
    MESSAGE_DUMP_CHAT = int(MESSAGE_DUMP_CHAT)

LOG_GROUP_ID = environ.get('LOG_GROUP_ID', '')
if len(LOG_GROUP_ID) == 0:
    print("LOG_GROUP_ID variable is missing! Exiting now")
    exit(1)
else:
    LOG_GROUP_ID = int(LOG_GROUP_ID)

GBAN_LOG_GROUP_ID = environ.get('GBAN_LOG_GROUP_ID', '')
if len(GBAN_LOG_GROUP_ID) == 0:
    print("GBAN_LOG_GROUP_ID variable is missing! Exiting now")
    exit(1)
else:
    GBAN_LOG_GROUP_ID = int(GBAN_LOG_GROUP_ID)

USERBOT_PREFIX = environ.get('USERBOT_PREFIX', '')
if len(USERBOT_PREFIX) == 0:
    USERBOT_PREFIX = "."

PHONE_NUMBER = environ.get('PHONE_NUMBER', '')
if len(PHONE_NUMBER) == 0:
    PHONE_NUMBER = None

SESSION_STRING = environ.get('SESSION_STRING', '')
if len(SESSION_STRING) == 0:
    SESSION_STRING = None

if PHONE_NUMBER:
    app2 = Client("userbot", phone_number=PHONE_NUMBER, api_id=API_ID, api_hash=API_HASH)
elif SESSION_STRING:
    app2 = Client('userbot', api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    print("PHONE_NUMBER or SESSION_STRING is required for start bot.")
    exit(1)

aid = environ.get('SUDO_USERS_ID', '')
if len(aid) != 0:
    aid = aid.split()
    SUDO_USERS_ID = {int(_id.strip()) for _id in aid} # Sudo users have full access to everything, don't trust anyone
else:
    SUDO_USERS_ID = set()

WELCOME_DELAY_KICK_SEC = environ.get('WELCOME_DELAY_KICK_SEC', '')
if len(WELCOME_DELAY_KICK_SEC) == 0:
    WELCOME_DELAY_KICK_SEC = 300
else:
    WELCOME_DELAY_KICK_SEC = int(WELCOME_DELAY_KICK_SEC)

RSS_DELAY = environ.get('RSS_DELAY', '')
RSS_DELAY = 300 if len(RSS_DELAY) == 0 else int(RSS_DELAY)

PM_PERMIT = environ.get('PM_PERMIT', '')
PM_PERMIT = PM_PERMIT.lower() in ['true', '1']

LOG_MENTIONS = environ.get('LOG_MENTIONS', '')
LOG_MENTIONS = LOG_MENTIONS.lower() in ['true', '1']

MOD_LOAD = []
MOD_NOLOAD = []
SUDOERS = filters.user()
bot_start_time = time()

class Log:
    def __init__(self, save_to_file=False, file_name="wbb.log"):
        self.save_to_file = save_to_file
        self.file_name = file_name

    def info(self, msg):
        print(f"[+]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[INFO]({ctime(time())}): {msg}\n")

    def error(self, msg):
        print(f"[-]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[ERROR]({ctime(time())}): {msg}\n")


log = Log(True, "bot.log")

# MongoDB client
log.info("Initializing MongoDB client")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.wbb


async def load_sudoers():
    global SUDOERS
    log.info("Loading sudoers")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = sudoers["sudoers"] if sudoers else []
    for user_id in SUDO_USERS_ID:
        SUDOERS.add(user_id)
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)


loop = get_event_loop()
loop.run_until_complete(load_sudoers())

aiohttpsession = ClientSession()

arq = ARQ("https://arq.hamker.in", ARQ_API_KEY, aiohttpsession)

app = Client("wbb", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

log.info("Starting bot client")
app.start()
log.info("Starting userbot client")
app2.start()

log.info("Gathering profile info")
x = app.get_me()
y = app2.get_me()

BOT_ID = x.id
BOT_NAME = x.first_name + (x.last_name or "")
BOT_USERNAME = x.username
BOT_MENTION = x.mention
BOT_DC_ID = x.dc_id

USERBOT_ID = y.id
USERBOT_NAME = y.first_name + (y.last_name or "")
USERBOT_USERNAME = y.username
USERBOT_MENTION = y.mention
USERBOT_DC_ID = y.dc_id

if USERBOT_ID not in SUDOERS:
    SUDOERS.add(USERBOT_ID)

log.info("Initializing Telegraph client")
try:
    telegraph = Telegraph()
    telegraph.create_account(short_name=BOT_USERNAME)
except Exception as e:
    log.error(f"Initializing Telegraph is failed: {e}")
    telegraph = None


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
