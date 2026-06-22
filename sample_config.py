"""
Sample Configuration File for WilliamButcherBot

Rename this to config.py and update with your values.
If config.py is not found, sample_config.py will be used as fallback.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

# Load from config.env if it exists, otherwise sample_config.env
load_dotenv(
    "config.env" if os.path.isfile("config.env") else "sample_config.env"
)

# ============ TELEGRAM BOT CONFIGURATION ============
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
USERBOT_PREFIX = os.environ.get("USERBOT_PREFIX", "\\")

# ============ USER PERMISSIONS ============
SUDO_USERS_ID = list(map(int, os.environ.get("SUDO_USERS_ID", "").split()))

# ============ LOGGING CONFIGURATION ============
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID"))
GBAN_LOG_GROUP_ID = int(os.environ.get("GBAN_LOG_GROUP_ID"))
MESSAGE_DUMP_CHAT = int(os.environ.get("MESSAGE_DUMP_CHAT"))

# ============ DATABASE CONFIGURATION ============
# PostgreSQL connection string (replaces MONGO_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# ============ EXTERNAL SERVICES ============
ARQ_API_KEY = os.environ.get("ARQ_API_KEY")
ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.dev")

# ============ BOT FEATURES ============
WELCOME_DELAY_KICK_SEC = int(os.environ.get("WELCOME_DELAY_KICK_SEC", 600))
LOG_MENTIONS = os.environ.get("LOG_MENTIONS", "True").lower() in ["true", "1"]
RSS_DELAY = int(os.environ.get("RSS_DELAY", 300))
PM_PERMIT = os.environ.get("PM_PERMIT", "True").lower() in ["true", "1"]

# ============ APPLICATION SETTINGS ============
TZ = os.environ.get("TZ", "Asia/Amman")
MAX_CONCURRENT_TASKS = int(os.environ.get("MAX_CONCURRENT_TASKS", "2"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "false").lower() in ["true", "1"]
