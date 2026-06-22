"""
Sample Configuration File for WilliamButcherBot

Rename this to config.py and update with your values.
If config.py is not found, sample_config.py will be used as fallback.
"""
import os
import sys

from dotenv import load_dotenv

# Load from config.env if it exists, otherwise sample_config.env
load_dotenv(
    "config.env" if os.path.isfile("config.env") else "sample_config.env"
)

# ── Raw reads (all safe, no int() yet) ────────────────────────────────────────
_BOT_TOKEN        = os.environ.get("BOT_TOKEN", "").strip()
_API_ID           = os.environ.get("API_ID", "").strip()
_API_HASH         = os.environ.get("API_HASH", "").strip()
_SESSION_STRING   = os.environ.get("SESSION_STRING", "").strip()
_PHONE_NUMBER     = os.environ.get("PHONE_NUMBER", "").strip()
_SUDO_USERS_ID    = os.environ.get("SUDO_USERS_ID", "").strip()
_LOG_GROUP_ID     = os.environ.get("LOG_GROUP_ID", "").strip()
_GBAN_LOG_GROUP_ID = os.environ.get("GBAN_LOG_GROUP_ID", "").strip()
_MESSAGE_DUMP_CHAT = os.environ.get("MESSAGE_DUMP_CHAT", "").strip()
_DATABASE_URL     = os.environ.get("DATABASE_URL", "").strip()

# ── Startup validation ─────────────────────────────────────────────────────────
# Collects every missing / invalid variable and prints a clear report
# before crashing, so Railway logs are immediately actionable.

REQUIRED_VARS = [
    ("BOT_TOKEN",          _BOT_TOKEN,          "Telegram bot token from @BotFather"),
    ("API_ID",             _API_ID,             "Telegram API ID from https://my.telegram.org"),
    ("API_HASH",           _API_HASH,           "Telegram API hash from https://my.telegram.org"),
    ("DATABASE_URL",       _DATABASE_URL,       "PostgreSQL connection string, e.g. postgresql://user:pass@host/db"),
    ("LOG_GROUP_ID",       _LOG_GROUP_ID,       "Telegram group ID (negative int) for bot logs"),
    ("GBAN_LOG_GROUP_ID",  _GBAN_LOG_GROUP_ID,  "Telegram group ID (negative int) for global-ban logs"),
    ("MESSAGE_DUMP_CHAT",  _MESSAGE_DUMP_CHAT,  "Telegram chat ID for message dumps"),
    ("SUDO_USERS_ID",      _SUDO_USERS_ID,      "Space-separated list of admin Telegram user IDs, e.g. 123456 789012"),
]

# SESSION_STRING or PHONE_NUMBER — at least one must be present
NEEDS_AUTH = not _SESSION_STRING and not _PHONE_NUMBER

_errors: list[str] = []

for var_name, value, hint in REQUIRED_VARS:
    if not value:
        _errors.append(f"  ✗  {var_name:25s}  — {hint}")

if NEEDS_AUTH:
    _errors.append(
        "  ✗  SESSION_STRING            — Pyrogram session string (recommended for Railway).\n"
        "                                  Generate locally with: python str_gen.py\n"
        "     OR\n"
        "  ✗  PHONE_NUMBER              — Phone number for interactive auth (NOT suitable for Railway)"
    )

# Integer validation for vars that must be integers
_int_vars = [
    ("API_ID",             _API_ID),
    ("LOG_GROUP_ID",       _LOG_GROUP_ID),
    ("GBAN_LOG_GROUP_ID",  _GBAN_LOG_GROUP_ID),
    ("MESSAGE_DUMP_CHAT",  _MESSAGE_DUMP_CHAT),
]
for var_name, raw in _int_vars:
    if raw and not raw.lstrip("-").isdigit():
        _errors.append(
            f"  ✗  {var_name:25s}  — must be an integer (got: {raw!r})"
        )

if _errors:
    print("\n" + "=" * 70)
    print("  STARTUP FAILED — Missing or invalid environment variables")
    print("=" * 70)
    for err in _errors:
        print(err)
    print("=" * 70)
    print("  Set these variables in Railway → Variables tab, then redeploy.")
    print("=" * 70 + "\n")
    sys.exit(1)

# ── Type-safe assignment (validation passed, so these are all safe) ────────────
BOT_TOKEN          = _BOT_TOKEN
API_ID             = int(_API_ID)
API_HASH           = _API_HASH
SESSION_STRING     = _SESSION_STRING        # may be empty string (PHONE_NUMBER path)
PHONE_NUMBER       = _PHONE_NUMBER or None
DATABASE_URL       = _DATABASE_URL
LOG_GROUP_ID       = int(_LOG_GROUP_ID)
GBAN_LOG_GROUP_ID  = int(_GBAN_LOG_GROUP_ID)
MESSAGE_DUMP_CHAT  = int(_MESSAGE_DUMP_CHAT)

# SUDO_USERS_ID — parse the space-separated list, skip blanks
try:
    SUDO_USERS_ID = [int(uid) for uid in _SUDO_USERS_ID.split() if uid.strip()]
except ValueError as exc:
    print(f"\n[CONFIG ERROR] SUDO_USERS_ID contains a non-integer value: {exc}")
    print("  Expected format: SUDO_USERS_ID=123456 789012\n")
    sys.exit(1)

# ── Optional / defaulted vars ──────────────────────────────────────────────────
USERBOT_PREFIX         = os.environ.get("USERBOT_PREFIX", "\\")
ANTHROPIC_API_KEY      = os.environ.get("ANTHROPIC_API_KEY", "")
ARQ_API_URL            = os.environ.get("ARQ_API_URL", "https://arq.hamker.dev")
WELCOME_DELAY_KICK_SEC = int(os.environ.get("WELCOME_DELAY_KICK_SEC", 600))
LOG_MENTIONS           = os.environ.get("LOG_MENTIONS", "True").lower() in ["true", "1"]
RSS_DELAY              = int(os.environ.get("RSS_DELAY", 300))
PM_PERMIT              = os.environ.get("PM_PERMIT", "True").lower() in ["true", "1"]
TZ                     = os.environ.get("TZ", "Asia/Amman")
MAX_CONCURRENT_TASKS   = int(os.environ.get("MAX_CONCURRENT_TASKS", "2"))
LOG_LEVEL              = os.environ.get("LOG_LEVEL", "false").lower() in ["true", "1"]
