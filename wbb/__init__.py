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

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
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
# Core configuration
USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT

# New environment variables
TZ = os.environ.get("TZ", "Asia/Amman")
MAX_CONCURRENT_TASKS = int(os.environ.get("MAX_CONCURRENT_TASKS", "2"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "false").lower() in ["true", "1"]

# Module loading
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
        
        # Console handler
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if self.save_to_file:
            file_handler = logging.FileHandler(self.file_name)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, msg: str) -> None:
        """Log info message."""
        print(f"[+]: {msg}")
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        """Log error message."""
        print(f"[-]: {msg}")
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        """Log debug message."""
        if LOG_LEVEL:
            print(f"[D]: {msg}")
            self.logger.debug(msg)


log = Log(True, "bot.log")

# ============ DATABASE INITIALIZATION ============
log.info("Initializing PostgreSQL database connection")

from wbb.core.database import DatabasePool
from wbb.utils.db_migrate import DatabaseMigrator

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    log.error("DATABASE_URL environment variable not set!")
    raise RuntimeError("DATABASE_URL is required")

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


# Initialize database at import time
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(init_database())
except Exception as e:
    log.error(f"Failed to initialize database: {e}")
    raise

# ============ MONGODB COMPATIBILITY LAYER ============
# For transitional compatibility, provide database collection objects
class DatabaseCollections:
    """Provides MongoDB-like access to PostgreSQL tables."""

    def __init__(self, pool: DatabasePool):
        self.pool = pool
        self._collections = {}

    def __getattr__(self, table_name: str):
        """Dynamically create collection-like objects for tables."""
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
    
    # Add from config
    for user_id in SUDO_USERS_ID:
        SUDOERS.add(user_id)
        if user_id not in sudoers_list:
            sudoers_list.append(user_id)
    
    # Update database
    if sudoers_list:
        await sudoersdb.update_one({"id": 1}, {"sudoers": sudoers_list}, upsert=True)
    
    # Add all from database to filter
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

aiohttpsession = ClientSession()
arq = ARQ(ARQ_API_URL, ANTHROPIC_API_KEY, aiohttpsession)
app = Client("sessions/wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

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
telegraph = Telegraph(domain="graph.org")
telegraph.create_account(short_name=BOT_USERNAME)


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
    await aiohttpsession.close()
    await db_pool.disconnect()
    log.info("Shutdown complete")
