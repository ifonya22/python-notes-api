from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://root:example@localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.notes_app


async def get_mongo_db():
    return db
