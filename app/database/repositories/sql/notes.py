from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.base import NoteRepository


class SQLNoteRepositoryImpl(NoteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_by_user_id(self, user_id: int) -> list[dict]:
        raise NotImplementedError

    async def get_by_note_id(self, note_id: str) -> Optional[dict]:
        raise NotImplementedError

    async def create(self, note: dict) -> dict:
        raise NotImplementedError

    async def delete(self, note_id: str) -> bool:
        raise NotImplementedError
