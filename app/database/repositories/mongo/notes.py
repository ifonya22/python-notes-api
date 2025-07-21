import datetime
from typing import Any, List, Optional

from app.database.repositories.base import NoteRepository
from app.utils.fields import PyObjectId


class MongoDBNoteRepositoryImpl(NoteRepository):
    def __init__(self, collection):
        self.collection = collection

    async def get_all(self) -> List[dict]:
        cursor = self.collection.find()
        return [doc async for doc in cursor]

    async def get_all_by_user_id(self, user_id: int) -> List[dict]:
        cursor = self.collection.find({"user_id": user_id})
        return [doc async for doc in cursor]

    async def get_by_note_id(self, note_id: PyObjectId) -> Optional[dict]:
        return await self.collection.find_one({"_id": note_id})

    async def get_by_note_id_and_user_id(self, note_id: PyObjectId, user_id: int) -> Optional[dict[str, Any]]:
        return await self.collection.find_one({"_id": note_id, "user_id": user_id})

    async def create(self, note: dict) -> dict:
        now = datetime.datetime.now(tz=datetime.UTC)
        note["is_deleted"] = False
        note["created_at"] = now
        note["updated_at"] = now
        await self.collection.insert_one(note)
        return note

    async def soft_delete(self, note_id: PyObjectId, user_id: int) -> bool:
        result = await self.collection.update_one(
            {"_id": note_id, "user_id": user_id},
            {"$set": {"is_deleted": True, "updated_at": datetime.datetime.now(tz=datetime.UTC)}},
        )
        return result.modified_count > 0

    async def restore(self, note_id: PyObjectId) -> bool:
        result = await self.collection.update_one(
            {"_id": note_id, "is_deleted": True},
            {"$set": {"is_deleted": False, "updated_at": datetime.datetime.now(tz=datetime.UTC)}},
        )
        return result.modified_count > 0

    async def update(self, note_id: PyObjectId, user_id: int, update_data: dict) -> dict[str, Any]:
        update_data.pop("_id", None)

        update_data["updated_at"] = datetime.datetime.now(tz=datetime.UTC)

        result = await self.collection.update_one(
            {"_id": note_id, "user_id": user_id, "is_deleted": False}, {"$set": update_data}
        )
        if result.modified_count > 0:
            return await self.collection.find_one({"_id": note_id, "user_id": user_id})
        return {}
