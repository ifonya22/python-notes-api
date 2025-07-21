from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

MONGO_URI = settings.mongo.mongo_uri
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db = client.notes_app


async def get_mongo_db():
    return db
