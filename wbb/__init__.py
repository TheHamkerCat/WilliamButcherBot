from pyrogram import Client
from configparser import ConfigParser
import logging
import time


f = open("error.log", "w")
f.write("PEAK OF LOG FILE")

LOG_FORMAT = (
    '''
    [%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s
    %(levelname)s: %(message)s'''
    )

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
NEOFETCH = (config.get("admin", "neofetch"))
Command = config.get("prefix", "prefixes").split()
MOD_LOAD = config.get("mods", "load_modules").split()
MOD_NOLOAD = config.get("mods", "noload_modules").split()
bot_start_time = time.time()


app = Client(":memory:", workers=16)
