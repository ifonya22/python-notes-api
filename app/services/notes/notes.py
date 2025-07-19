import datetime

from fastapi import HTTPException

from app.api.v1.notes.schemas import (
    CreateNoteRequestV1,
    NoteResponseAdminV1,
    NoteResponseV1,
    UpdateNoteRequestV1,
)
from app.database.repositories.base import NoteRepository
from app.utils.fields import PyObjectId


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    async def create_note(self, note: CreateNoteRequestV1, user_id: int) -> NoteResponseV1:
        doc = note.model_dump()
        doc["user_id"] = user_id
        doc["is_deleted"] = False
        doc["created_at"] = datetime.datetime.now(tz=datetime.UTC)
        doc["updated_at"] = datetime.datetime.now(tz=datetime.UTC)

        result = await self.note_repo.create(doc)

        return NoteResponseV1(**result)

    async def get_note_by_note_id_and_user_id(self, note_id: PyObjectId, user_id: int) -> NoteResponseV1:
        result = await self.note_repo.get_by_note_id_and_user_id(note_id, user_id)

        if not result:
            raise HTTPException(status_code=401, detail="Note was not founded!")

        if result["is_deleted"]:
            raise HTTPException(status_code=401, detail=f"Note {result['_id']} was deleted!")

        return NoteResponseV1(**result)

    async def get_note_by_note_id(self, note_id: PyObjectId) -> NoteResponseAdminV1:
        result = await self.note_repo.get_by_note_id(note_id)

        if not result:
            raise HTTPException(status_code=401, detail="Note was not founded!")

        if result["is_deleted"]:
            raise HTTPException(status_code=401, detail=f"Note {result['_id']} was deleted!")

        return NoteResponseAdminV1(**result)

    async def get_all_notes_by_user_id(
        self, user_id: int, is_admin: bool = False
    ) -> list[NoteResponseV1] | list[NoteResponseAdminV1]:
        results = await self.note_repo.get_all_by_user_id(user_id=user_id)
        if is_admin:
            return [NoteResponseAdminV1(**result) for result in results]
        return [NoteResponseV1(**result) for result in results if not result["is_deleted"]]

    async def get_all_notes(self) -> list[NoteResponseAdminV1]:
        results = await self.note_repo.get_all()

        return [NoteResponseAdminV1(**result) for result in results]

    async def delete_note_by_note_id_and_user_id(self, note_id: PyObjectId, user_id: int) -> bool:
        result = await self.note_repo.soft_delete(note_id, user_id)
        if not result:
            raise HTTPException(status_code=401, detail=f"Note {result['note_id']} was not deleted!")
        return result

    async def restore_note_by_note_id(self, note_id: PyObjectId) -> bool:
        result = await self.note_repo.restore(note_id)
        if not result:
            raise HTTPException(status_code=401, detail=f"Note {result['note_id']} was not restored!")
        return result

    async def update_note_by_id(self, note_id: PyObjectId, user_id: int, update_data: UpdateNoteRequestV1) -> bool:
        result = await self.note_repo.update(note_id, user_id, update_data.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=401, detail=f"Note {result['note_id']} was not restored!")
        return NoteResponseV1(**result)
