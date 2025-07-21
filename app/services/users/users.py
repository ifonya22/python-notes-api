from fastapi import HTTPException

from app.api.v1.users.schemas import (
    CreateUserV1,
    RegisterResponseV1,
)
from app.database.repositories.base import UserRepository
from app.exceptions import UserAlreadyExistExc
from app.schemas.users import CreateUserDTO
from app.services.auth import utils as auth_utils


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, user_data: CreateUserV1) -> RegisterResponseV1:
        try:
            hashed_password = auth_utils.hash_password(user_data.password)
            db_user = await self.user_repo.create(
                CreateUserDTO(
                    username=user_data.username,
                    password=hashed_password,
                )
            )
            return RegisterResponseV1.model_validate(db_user)
        except UserAlreadyExistExc:
            raise HTTPException(status_code=401, detail="User already exist")

    async def switch_role(self, username: str, user_role: str):
        result = "user"
        if user_role == "admin":
            result = await self.user_repo.set_user_role(username, "user")
        elif user_role == "user":
            result = await self.user_repo.set_user_role(username, "admin")
        return result
