from pyrogram import Client
from configparser import ConfigParser
import logging
import os


if os.path.exists("wbb/logs/error.log"):
    f = open("wbb/logs/error.log", "w")
    f.write("PEAK OF LOG FILE")

LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%m-%d %H:%M",
    filename="wbb/logs/error.log",
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
OWNER_ID = config.get("admin", "owner_id")
Command = config.get("prefix", "prefixes").split()
MOD_LOAD = config.get("mods", "load_modules").split()
MOD_NOLOAD = config.get("mods", "noload_modules").split()


app = Client(
    ":memory:"
)






