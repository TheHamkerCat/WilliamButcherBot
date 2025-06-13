import os

from dotenv import load_dotenv

load_dotenv(
    "config.env" if os.path.isfile("config.env") else "sample_config.env"
)

BOT_TOKEN = os.environ.get("7843703186:AAFO-nNbqSc2ndcKkinqj0oD-qdm2EanfCU")
API_ID = int(os.environ.get("25431765"))
SESSION_STRING = os.environ.get("BQGEDtUAu7GqSQ0Gq3l4D0htelarr2gqfQi9btAZy1GPTBIQAcKIESia-TA5hK8tyg80SejpwBZbeJWttVZ0UF-sc_72YAn9l8FIS_N7oJbe-93PaIcovkRRCho8Kw8oLwhPenlnmXudjWSkxYfvyYB57ujgtFyI4-KSi2-N3VAYNWGwmmKkQTtEMQvags2NkoUjWRFxAd8s3_VHaePDqkbMNfYb005FKgHsgNgkz_T96XjZR3praxOorKu0UogvYCUtFVCR3U_mtYRIRRoXHehypuLJIOcWVEicQ0OK_GGVFKLhj45IM8UVniW9GaVzxmtYbJxOKByurobs9B0hsq68qCEpwwAAAAGof67WAA", "")
API_HASH = os.environ.get("f86261c85d80a06b9d5824f9186b7427")
USERBOT_PREFIX = os.environ.get("USERBOT_PREFIX", "\\")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
SUDO_USERS_ID = list(map(int, os.environ.get("6853231635", "").split()))
LOG_GROUP_ID = int(os.environ.get("-1002598297381"))
GBAN_LOG_GROUP_ID = int(os.environ.get("-1002598297381"))
MESSAGE_DUMP_CHAT = int(os.environ.get("-1002598297381"))
WELCOME_DELAY_KICK_SEC = int(os.environ.get("WELCOME_DELAY_KICK_SEC", 600))
MONGO_URL = os.environ.get("mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
ARQ_API_KEY = os.environ.get("GXAWUH-PARFUC-RPGWZJ-KTDATF-ARQ")
ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.dev")
LOG_MENTIONS = os.environ.get("LOG_MENTIONS", "True").lower() in ["true", "1"]
RSS_DELAY = int(os.environ.get("RSS_DELAY", 300))
PM_PERMIT = os.environ.get("PM_PERMIT", "True").lower() in ["true", "1"]
