from fastapi import APIRouter, Depends

from app.api.deps import get_mongo_note_service
from app.api.enums import Roles
from app.config.config import get_logger
from app.schemas.users import UserInDBDTO
from app.services.notes.notes import NoteService
from app.utils.fields import PyObjectId

from .schemas import (
    CreateNoteRequestV1,
    NoteResponseV1,
    UpdateNoteRequestV1,
)

router = APIRouter()
logger = get_logger()


@router.post(
    "/",
    status_code=201,
    name="Создание новой заметки",
    description="""
    Создаёт новую заметку для текущего авторизованного пользователя.
    Возвращает созданную заметку с присвоенным id""",
)
async def create_note(
    request: CreateNoteRequestV1,
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> NoteResponseV1:
    logger.info(
        f"[{current_user.role} (id: {current_user.id})] Запрашивает создание заметки ({request.title=}, {request.body=})"
    )
    result = await note_service.create_note(note=request, user_id=current_user.id)
    logger.info(f"[{current_user.role} (id: {current_user.id})] Создал заметку ID: {result.note_id}")
    return result


@router.get(
    "/",
    name="Получение всех заметок пользователя",
    description="Возвращает список всех заметок текущего авторизованного пользователя",
)
async def get_all_notes(
    current_user: UserInDBDTO = Depends(Roles.USER_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> list[NoteResponseV1]:
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает все заметки")
    result = await note_service.get_all_notes_by_user_id(user_id=current_user.id)
    logger.info(
        f"[{current_user.role} (id: {current_user.id})] Получил заметок {len(result)}:{[str(r.note_id) for r in result]}"
    )
    return result


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
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает заметку ID: {note_id}")
    note = await note_service.get_note_by_note_id_and_user_id(note_id=note_id, user_id=current_user.id)
    logger.info(f"[{current_user.role} (id: {current_user.id})] Получил заметку ID: {note_id}")
    return note


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
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает обновление заметки ID: {note_id}")
    updated_note = await note_service.update_note_by_id(note_id=note_id, user_id=current_user.id, update_data=request)
    logger.info(f"[{current_user.role} (id: {current_user.id})] Обновил заметку ID: {note_id}")
    return updated_note


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
    logger.warning(f"[{current_user.role} (id: {current_user.id})] Запрашивает удаление заметки ID: {note_id}")
    await note_service.delete_note_by_note_id_and_user_id(note_id=note_id, user_id=current_user.id)
    logger.warning(f"[{current_user.role} (id: {current_user.id})] Удалил заметку ID: {note_id}")
    return None
