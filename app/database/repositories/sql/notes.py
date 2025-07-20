from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.base import NoteRepository
from app.utils.fields import PyObjectId


class SQLNoteRepositoryImpl(NoteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_by_user_id(self, user_id: int) -> list[dict]:
        raise NotImplementedError

    async def get_by_note_id(self, note_id: str) -> Optional[dict]:
        raise NotImplementedError

    async def create(self, note: dict) -> dict:
        raise NotImplementedError

    async def get_all(self) -> list[dict]:
        raise NotImplementedError

    async def get_by_note_id_and_user_id(self, note_id: PyObjectId, user_id: int) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    async def soft_delete(self, note_id: PyObjectId, user_id: int) -> bool:
        raise NotImplementedError

    async def restore(self, note_id: PyObjectId) -> bool:
        raise NotImplementedError

    async def update(self, note_id: PyObjectId, user_id: int, update_data: dict) -> dict[str, Any]:
        raise NotImplementedError
