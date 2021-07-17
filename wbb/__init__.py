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
print("[INFO]: INITIALIZING")
import asyncio
import logging
import time
from os import path

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from Python_ARQ import ARQ

# Setup logging
log_file = "error.log"

with open(log_file, "w") as f:
    f.write("PEAK OF LOG FILE")
logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    filename=log_file,
    filemode="w",
)
console = logging.StreamHandler()
logging.getLogger("").addHandler(console)
log = logging.getLogger()

is_config = path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
SUDOERS = SUDO_USERS_ID
FERNET_ENCRYPTION_KEY = FERNET_ENCRYPTION_KEY
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

# MongoDB client
print("[INFO]: INITIALIZING DATABASE")
mongo_client = MongoClient(MONGO_DB_URI)
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
    print("[INFO]: INITIALIZING USERBOT CLIENT")
    app2 = Client(
        "userbot",
        phone_number=PHONE_NUMBER,
        api_id=API_ID,
        api_hash=API_HASH,
    )
else:
    print("[INFO]: INITIALIZING USERBOT CLIENT")
    app2 = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
# Bot client
print("[INFO]: INITIALIZING BOT CLIENT")
app = Client(
    "wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH
)


BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
BOT_MENTION = ""
BOT_DC_ID = 0
USERBOT_ID = 0
USERBOT_NAME = ""
USERBOT_USERNAME = ""
USERBOT_DC_ID = 0
USERBOT_MENTION = ""
USERBOT_BOT_CHAT_COMMON = []


def get_info(app, app2):
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_DC_ID, BOT_MENTION
    global USERBOT_ID, USERBOT_NAME, USERBOT_USERNAME, USERBOT_DC_ID, USERBOT_MENTION
    global USERBOT_BOT_CHAT_COMMON
    getme = app.get_me()
    getme2 = app2.get_me()
    BOT_ID = getme.id
    USERBOT_ID = getme2.id
    BOT_NAME = (
        f"{getme.first_name} {getme.last_name}"
        if getme.last_name
        else getme.first_name
    )
    BOT_USERNAME = getme.username
    BOT_MENTION = getme.mention
    BOT_DC_ID = getme.dc_id

    USERBOT_NAME = (
        f"{getme2.first_name} {getme2.last_name}"
        if getme2.last_name
        else getme2.first_name
    )
    USERBOT_USERNAME = getme2.username
    USERBOT_MENTION = getme2.mention
    USERBOT_DC_ID = getme2.dc_id


print("[INFO]: STARTING BOT CLIENT TEMPORARILY")
app.start()
print("[INFO]: STARTING USERBOT CLIENT TEMPORARILY")
app2.start()
print("[INFO]: LOADING UB/BOT PROFILE INFO")
get_info(app, app2)
print("[INFO]: LOADED UB/BOT PROFILE INFO")
if USERBOT_ID not in SUDOERS:
    SUDOERS.append(USERBOT_ID)
app.stop()
app2.stop()
