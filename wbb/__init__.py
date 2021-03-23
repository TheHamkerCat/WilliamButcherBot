from config import (
    BOT_TOKEN, API_ID ,API_HASH, OWNER_ID, SUDO_USER_ID,
    LOG_GROUP_ID, FERNET_ENCRYPTION_KEY, MONGO_DB_URI,
    WELCOME_DELAY_KICK_SEC, ARQ_API_BASE_URL as ARQ_API,
    SUDO_CHAT_ID
    )
from pyrogram import Client
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


SUDOERS = SUDO_USER_ID
SUDOERS.append(OWNER_ID)
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.wbb
app = Client("wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
arq = ARQ(ARQ_API)
