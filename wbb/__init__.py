# flake8: noqa F405
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
import asyncio
import time
from inspect import getfullargspec
from os import path

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph

is_config = path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
SUDOERS = SUDO_USERS_ID
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

# MongoDB client
print("[INFO]: INITIALIZING DATABASE")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.wbb


async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDOERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS
    print("[INFO]: LOADED SUDOERS")


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

if not HEROKU:
    app2 = Client(
        "userbot",
        phone_number=PHONE_NUMBER,
        api_id=API_ID,
        api_hash=API_HASH,
    )
else:
    app2 = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = Client("wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

print("[INFO]: STARTING BOT CLIENT")
app.start()
print("[INFO]: STARTING USERBOT CLIENT")
app2.start()

print("[INFO]: GATHERING PROFILE INFO")
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
    SUDOERS.append(USERBOT_ID)

telegraph = Telegraph()
telegraph.create_account(short_name=BOT_USERNAME)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
