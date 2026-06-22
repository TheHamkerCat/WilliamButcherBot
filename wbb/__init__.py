"""
MIT License

Copyright (c) 2024 TheHamkerCat

WilliamButcherBot - Telegram Group Manager Bot
"""
import asyncio
import logging
import os
import time
from inspect import getfullargspec
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message
from pyromod import listen
from telegraph import Telegraph

# ============ CONFIGURATION LOADING ============
is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

# Create sessions directory
Path("sessions").mkdir(exist_ok=True)

# ============ ENVIRONMENT VARIABLES ============
USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT

TZ = os.environ.get("TZ", "Asia/Amman")
MAX_CONCURRENT_TASKS = int(os.environ.get("MAX_CONCURRENT_TASKS", "2"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "false").lower() in ["true", "1"]

MOD_LOAD = []
MOD_NOLOAD = []
SUDOERS = filters.user()
bot_start_time = time.time()

# ============ LOGGING SETUP ============
class Log:
    """Simple logging handler."""

    def __init__(self, save_to_file=False, file_name="wbb.log"):
        self.save_to_file = save_to_file
        self.file_name = file_name
        self.logger = logging.getLogger("wbb")

        if LOG_LEVEL:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if self.save_to_file:
            file_handler = logging.FileHandler(self.file_name)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, msg: str) -> None:
        print(f"[+]: {msg}")
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        print(f"[-]: {msg}")
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        if LOG_LEVEL:
            print(f"[D]: {msg}")
            self.logger.debug(msg)


log = Log(True, "bot.log")

# ============ DATABASE INITIALIZATION ============
log.info("Initializing PostgreSQL database connection")

from wbb.core.database import DatabasePool
from wbb.utils.db_migrate import DatabaseMigrator

db_pool = DatabasePool(DATABASE_URL)


async def init_database():
    """Initialize database connection and schema."""
    try:
        await db_pool.connect()
        log.info("Connected to PostgreSQL database")

        migrator = DatabaseMigrator(db_pool)
        await migrator.initialize()
        log.info("Database schema initialized")
    except Exception as e:
        log.error(f"Database initialization failed: {e}")
        raise


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(init_database())
except Exception as e:
    log.error(f"Failed to initialize database: {e}")
    raise

# ============ MONGODB COMPATIBILITY LAYER ============
class DatabaseCollections:
    """Provides MongoDB-like access to PostgreSQL tables."""

    def __init__(self, pool: DatabasePool):
        self.pool = pool
        self._collections = {}

    def __getattr__(self, table_name: str):
        if table_name not in self._collections:
            from wbb.core.database import MongoCompatibilityLayer
            self._collections[table_name] = MongoCompatibilityLayer(self.pool, table_name)
        return self._collections[table_name]


db = DatabaseCollections(db_pool)
log.info("Database collections initialized")


# ============ ASYNC OPERATIONS ============
async def load_sudoers():
    """Load sudoers from database."""
    global SUDOERS
    log.info("Loading sudoers from database")

    sudoersdb = db.sudoers
    sudoers_doc = await sudoersdb.find_one({"id": 1})
    sudoers_list = sudoers_doc.get("sudoers", []) if sudoers_doc else []

    for user_id in SUDO_USERS_ID:
        SUDOERS.add(user_id)
        if user_id not in sudoers_list:
            sudoers_list.append(user_id)

    # Cast to bigint list so asyncpg matches the BIGINT[] column type
    sudoers_list = [int(uid) for uid in sudoers_list]

    if sudoers_list:
        await sudoersdb.update_one({"id": 1}, {"sudoers": sudoers_list}, upsert=True)

    for user_id in sudoers_list:
        SUDOERS.add(user_id)


loop.run_until_complete(load_sudoers())

# ============ PYROGRAM CLIENTS ============
log.info("Initializing Pyrogram clients")

if not SESSION_STRING:
    app2 = Client(
        name="sessions/userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER,
    )
else:
    app2 = Client(
        name="sessions/userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )

app = Client("sessions/wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# ============ DEFERRED ASYNC RESOURCES ============
# These are initialized inside the running event loop in __main__.py
aiohttpsession = None
arq = None

# BOT/USERBOT info — populated after async start in __main__.py
BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None
BOT_MENTION = None
BOT_DC_ID = None

USERBOT_ID = None
USERBOT_NAME = None
USERBOT_USERNAME = None
USERBOT_MENTION = None
USERBOT_DC_ID = None

telegraph = None


# ============ UTILITY FUNCTIONS ============
async def eor(msg: Message, **kwargs):
    """Edit or reply - edits own messages, replies to others."""
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


# ============ GRACEFUL SHUTDOWN ============
async def shutdown():
    """Cleanup and shutdown."""
    log.info("Shutting down...")
    if aiohttpsession:
        await aiohttpsession.close()
    await db_pool.disconnect()
    log.info("Shutdown complete")
