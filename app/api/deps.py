from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_logger
from app.database.factory import RepositoryDBFactory
from app.database.mongo.client import get_mongo_db
from app.database.sql.session import get_sql_session
from app.schemas.users import UserInDBDTO
from app.services.auth import utils as auth_utils
from app.services.notes.notes import NoteService
from app.services.users.users import UserService

logger = get_logger()


def get_repository_db_factory(
    sql_session: AsyncSession = Depends(get_sql_session),
    mongo_db: MongoClient = Depends(get_mongo_db),
) -> RepositoryDBFactory:
    return RepositoryDBFactory(sql_session=sql_session, mongo_db=mongo_db)


def get_sql_user_service(db_factory: RepositoryDBFactory = Depends(get_repository_db_factory)) -> UserService:
    return UserService(db_factory.get_sql_user_repository())


def get_mongo_note_service(db_factory: RepositoryDBFactory = Depends(get_repository_db_factory)) -> NoteService:
    return NoteService(db_factory.get_mongo_note_repository())


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login/",
)


async def validate_auth_user(
    username: str = Form(...),
    password: str = Form(...),
    db_factory: RepositoryDBFactory = Depends(get_repository_db_factory),
) -> UserInDBDTO:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await db_factory.get_sql_user_repository().get_by_username(username)
    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(password, user.password):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")

    return user


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return auth_utils.decode_jwt(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db_factory: RepositoryDBFactory = Depends(get_repository_db_factory),
) -> UserInDBDTO:
    username = payload.get("sub")

    if not isinstance(username, str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username in token")

    user = await db_factory.get_sql_user_repository().get_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def get_current_active_auth_user(
    user: UserInDBDTO = Depends(get_current_auth_user),
) -> UserInDBDTO:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
    return user


def role_required(*allowed_roles):
    def dependency(current_user: UserInDBDTO = Depends(get_current_active_auth_user)) -> UserInDBDTO:
        if current_user.role not in allowed_roles:
            logger.warning(
                f"[{current_user.role} (id: {current_user.id})] Попытался получить доступ без роли {allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}",
            )
        return current_user

    return dependency
