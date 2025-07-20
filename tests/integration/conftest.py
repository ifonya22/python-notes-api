import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.database.repositories.mongo.notes import MongoDBNoteRepositoryImpl


@pytest.fixture(scope="session")
def docker_mongo():
    return settings.mongo.mongo_uri


@pytest_asyncio.fixture(scope="function")
async def async_mongo_client(docker_mongo):
    client = AsyncIOMotorClient(docker_mongo)
    yield client


@pytest_asyncio.fixture(scope="function")
async def note_repo(async_mongo_client):
    db = async_mongo_client["test_db"]
    collection = db["notes_test"]
    repo = MongoDBNoteRepositoryImpl(collection)
    print(type(repo))
    yield repo
    await collection.drop()
