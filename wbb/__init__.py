import logging
import time
from configparser import ConfigParser
from pyrogram import Client


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

config = ConfigParser()
config.read("config.ini")
OWNER_ID = int(config.get("admin", "owner_id"))
SUDO_USER_ID = int(config.get("admin", "sudo_user_id"))
LOG_GROUP_ID = int(config.get("admin", "log_group_id"))
NEOFETCH = config.get("admin", "neofetch")
WALL_API_KEY = config.get("admin", "alpha_coders_wall_api_key")
FERNET_ENCRYPTION_KEY = config.get("admin", "fernet_encryption_key")
WELCOME_DELAY_KICK_SEC = int(config.get("admin", "captcha_delay_in_seconds"))
JSMAPI = config.get("admin", "jio_saavn_api")
Command = config.get("prefix", "prefixes").split()
MOD_LOAD = config.get("mods", "load_modules").split()
MOD_NOLOAD = config.get("mods", "noload_modules").split()
bot_start_time = time.time()

app = Client("wbb", workers=16)
