from config import (
    BOT_TOKEN, API_ID, API_HASH, SUDO_USERS_ID, PHONE_NUMBER,
    LOG_GROUP_ID, FERNET_ENCRYPTION_KEY, MONGO_DB_URI,
    WELCOME_DELAY_KICK_SEC, ARQ_API_BASE_URL as ARQ_API,
    MAIN_CHATS
)
from pyrogram import Client
from pytgcalls import GroupCall
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Python_ARQ import ARQ
import time
import logging

f = open("error.log", "w")
f.write("PEAK OF LOG FILE")

LOG_FORMAT = (
    '''
    [%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s
    %(levelname)s: %(message)s''')

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%m-%d %H:%M",
    filename="error.log",
    filemode="w",
)

console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

log = logging.getLogger()

SUDOERS = SUDO_USERS_ID

def init_sudo():
    global SUDOERS
    from wbb.utils.botinfo import USERBOT_ID
    SUDOERS.append(USERBOT_ID)

FERNET_ENCRYPTION_KEY = FERNET_ENCRYPTION_KEY
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.wbb


# Userbot client
print("\nStarting Helper Userbot")
app2 = Client(
    "userbot",
    phone_number=PHONE_NUMBER,
    api_id=API_ID,
    api_hash=API_HASH
)


# Mainbot client
print("\nStarting Main Bot\n")
app = Client(
    "wbb",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Pytgcalls client
vc = GroupCall(
        app2,
        input_filename="input.raw",
        play_on_repeat=False,
        enable_logs_to_console=False
        )

# ARQ client
arq = ARQ(ARQ_API)
