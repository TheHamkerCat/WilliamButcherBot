from os import environ, path

from dotenv import load_dotenv

if path.exists('config.env'):
    load_dotenv("config.env")
    BOT_TOKEN = environ.get('BOT_TOKEN', '')
    if len(BOT_TOKEN) == 0:
        print("BOT_TOKEN variable is missing!")

    API_ID = environ.get('API_ID', '')
    if len(API_ID) == 0:
        print("API_ID variable is missing!")
    else:
        API_ID = int(API_ID)

    API_HASH = environ.get('API_HASH', '')
    if len(API_HASH) == 0:
        print("API_HASH variable is missing!")
    
    ARQ_API_URL = environ.get('ARQ_API_URL', 'https://arq.hamker.in')

    ARQ_API_KEY = environ.get('ARQ_API_KEY', '')
    if len(ARQ_API_KEY) == 0:
        print("ARQ_API_KEY variable is missing!\nGet this from @ARQRobot")

    MONGO_URL = environ.get('MONGO_URL', '')
    if len(MONGO_URL) == 0:
        print("MONGO_URL variable is missing!")

    MESSAGE_DUMP_CHAT = environ.get('MESSAGE_DUMP_CHAT', 0)

    LOG_GROUP_ID = environ.get('LOG_GROUP_ID', 0)

    GBAN_LOG_GROUP_ID = environ.get('GBAN_LOG_GROUP_ID', 0)

    USERBOT_PREFIX = environ.get('USERBOT_PREFIX', '.')

    PHONE_NUMBER = environ.get('PHONE_NUMBER', '')
    if len(PHONE_NUMBER) == 0:
        PHONE_NUMBER = None

    SESSION_STRING = environ.get('SESSION_STRING', '')
    if len(SESSION_STRING) == 0:
        SESSION_STRING = None

    # Sudo users have full access to everything, don't trust anyone
    SUDO_USERS_ID = {int(_id.strip()) for _id in environ.get('SUDO_USERS_ID').split()}

    WELCOME_DELAY_KICK_SEC = environ.get('WELCOME_DELAY_KICK_SEC', 300)

    RSS_DELAY = environ.get('RSS_DELAY', 300)

    PM_PERMIT = environ.get('PM_PERMIT', '')
    PM_PERMIT = PM_PERMIT.lower() in ['true', '1']

    LOG_MENTIONS = environ.get('LOG_MENTIONS', '')
    LOG_MENTIONS = LOG_MENTIONS.lower() in ['true', '1']
else:
    BOT_TOKEN = "467677575:YZfaakjwd545dfg-N6JStihhuw5gQeZHntc"
    API_ID = 123456
    SESSION_STRING = ""  # Check Readme to generate sessions; need for userbot
    API_HASH = "dfxcgs5s12hdcxfgdfz"
    USERBOT_PREFIX = "."
    PHONE_NUMBER = "+916969696969"  # Need for Userbot
    SUDO_USERS_ID = [
        4543744343,
        543214651351,
    ]  # Sudo users have full access to everything, don't trust anyone
    LOG_GROUP_ID = -100125431255
    GBAN_LOG_GROUP_ID = -100125431255
    MESSAGE_DUMP_CHAT = -1001181696437
    WELCOME_DELAY_KICK_SEC = 300
    MONGO_URL = "mongodb+srv://username:password@cluster0.ksiis.mongodb.net/YourDataBaseName?retryWrites=true&w=majority"
    ARQ_API_KEY = "Get this from @ARQRobot"
    ARQ_API_URL = "https://arq.hamker.in"
    LOG_MENTIONS = True
    RSS_DELAY = 300  # In seconds
    PM_PERMIT = True
