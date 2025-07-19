from fastapi import APIRouter, Depends

from app.api.deps import get_mongo_note_service
from app.api.enums import Roles
from app.config import get_logger
from app.schemas.users import UserInDBDTO
from app.services.notes.notes import NoteService
from app.utils.fields import PyObjectId

from .schemas import (
    NoteResponseAdminV1,
)

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    name="Получение всех заметок пользователя",
    description="""
    Возвращает список всех заметок указанного пользователя.
    
    Доступно только для администраторов""",
    response_description="Список заметок пользователя",
)
async def get_all_notes_by_user_id(
    user_id: int,
    current_user: UserInDBDTO = Depends(Roles.ADMIN_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> list[NoteResponseAdminV1]:
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает все заметки пользователя ID: {user_id}")
    result = await note_service.get_all_notes_by_user_id(user_id=user_id, is_admin=True)
    logger.info(
        f"[{current_user.role} (id: {current_user.id})] Получил все заметки пользователя ID: {user_id} (всего: {len(result)})"
    )
    return result


@router.get(
    "/all",
    name="Получение всех заметок в системе",
    description="""Возвращает список всех заметок всех пользователей. 
    
    Доступно только для администраторов""",
)
async def get_all_notes(
    current_user: UserInDBDTO = Depends(Roles.ADMIN_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> list[NoteResponseAdminV1]:
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает все заметки")
    result = await note_service.get_all_notes()
    logger.info(f"[{current_user.role} (id: {current_user.id})] Получил все заметки (всего: {len(result)})")
    return result


@router.get(
    "/{note_id}",
    name="Получение конкретной заметки по ID",
    description="""Возвращает информацию о заметке по её уникальному идентификатору вне зависимости от принадлежности к пользователю. 
    
    Доступно только для администраторов""",
)
async def get_note(
    note_id: PyObjectId,
    current_user: UserInDBDTO = Depends(Roles.ADMIN_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
) -> NoteResponseAdminV1:
    logger.info(f"[{current_user.role} (id: {current_user.id})] Запрашивает заметку ID: {note_id}")
    note = await note_service.get_note_by_note_id(note_id=note_id)
    logger.info(f"[{current_user.role} (id: {current_user.id})] Получил заметку ID: {note_id}")
    return note


@router.patch(
    "/{note_id}/restore",
    status_code=201,
    name="Восстановление удалённой заметки",
    description="""Восстанавливает ранее удалённую заметку.
     
    Доступно только для администраторов""",
)
async def restore_note(
    note_id: PyObjectId,
    current_user: UserInDBDTO = Depends(Roles.ADMIN_ONLY),
    note_service: NoteService = Depends(get_mongo_note_service),
):
    logger.warning(f"[{current_user.role} (id: {current_user.id})] Запрашивает восстановление заметки ID: {note_id}")
    await note_service.restore_note_by_note_id(note_id=note_id)
    logger.warning(f"[{current_user.role} (id: {current_user.id})] Восстановил заметку ID: {note_id}")
