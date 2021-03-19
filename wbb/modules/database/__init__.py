from motor.motor_asyncio import AsyncIOMotorClient
from ...config import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client.wbb
