from pyrogram import Client
from pyromod import listen
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Python_ARQ import ARQ
from os import path
import time

is_config = path.exists('config.py')
if is_config:
    from config import *
else:
    from sample_config import *

SUDOERS = SUDO_USERS_ID
MAIN_CHATS = MAIN_CHATS
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
FERNET_ENCRYPTION_KEY = FERNET_ENCRYPTION_KEY
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.wbb

if not HEROKU:
    app2 = Client(
        "userbot",
        phone_number=PHONE_NUMBER,
        api_id=API_ID,
        api_hash=API_HASH
    )
else:
    app2 = Client(
        SESSION_STRING,
        api_id=API_ID,
        api_hash=API_HASH
    )

app = Client(
    "wbb",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
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


def get_info(app, app2):
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_DC_ID, BOT_MENTION
    global USERBOT_ID, USERBOT_NAME, USERBOT_USERNAME, USERBOT_DC_ID, USERBOT_MENTION
    getme = app.get_me()
    getme2 = app2.get_me()
    BOT_ID = getme.id
    USERBOT_ID = getme2.id
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_MENTION = getme.mention
    BOT_DC_ID = getme.dc_id

    if getme2.last_name:
        USERBOT_NAME = getme2.first_name + " " + getme2.last_name
    else:
        USERBOT_NAME = getme2.first_name
    USERBOT_USERNAME = getme2.username
    USERBOT_MENTION = getme2.mention
    USERBOT_DC_ID = getme2.dc_id


app.start()
app2.start()
get_info(app, app2)
SUDOERS.append(USERBOT_ID)
# ARQ client
arq = ARQ(ARQ_API_BASE_URL)