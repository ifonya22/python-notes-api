from fastapi import APIRouter, Depends

from app.api.deps import get_mongo_note_service
from app.api.enums import Roles
from app.schemas.users import UserInDBDTO
from app.services.notes.notes import NoteService
from app.utils.fields import PyObjectId

from .schemas import (
    CreateNoteRequestV1,
    NoteResponseV1,
    UpdateNoteRequestV1,
)

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    name="Создание новой заметки",
    description="""
    Создаёт новую заметку для текущего авторизованного пользователя
    
    Возвращает созданную заметку с присвоенным id""",
)
async def create_note(
    request: CreateNoteRequestV1,
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> NoteResponseV1:
    return await note_service.create_note(note=request, user_id=current_user.id)


@router.get(
    "/",
    name="Получение всех заметок пользователя",
    description="Возвращает список всех заметок текущего авторизованного пользователя",
)
async def get_all_notes(
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> list[NoteResponseV1]:
    return await note_service.get_all_notes_by_user_id(user_id=current_user.id)


@router.get(
    "/{note_id}",
    name="Получение конкретной заметки по ID",
    description="Возвращает одну заметку по её уникальному идентификатору и идентификатору пользователя",
)
async def get_note(
    note_id: PyObjectId,
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> NoteResponseV1:
    return await note_service.get_note_by_note_id_and_user_id(note_id=note_id, user_id=current_user.id)


@router.patch(
    "/{note_id}",
    name="Обновление существующей заметки",
    description="Обновляет заголовок и/или содержимое заметки по её уникальному идентификатору",
)
async def update_note(
    note_id: PyObjectId,
    request: UpdateNoteRequestV1,
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> NoteResponseV1:
    return await note_service.update_note_by_id(note_id=note_id, user_id=current_user.id, update_data=request)


@router.delete(
    "/{note_id}",
    status_code=204,
    name="Удаление заметки",
    description="Удаляет заметку по её уникальному идентификатору. Возвращает статус 204 (No Content)",
)
async def delete_note(
    note_id: PyObjectId,
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> None:
    await note_service.delete_note_by_note_id_and_user_id(note_id=note_id, user_id=current_user.id)
    return None
