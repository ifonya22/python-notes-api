from typing import Optional

from app.database.repositories.base import UserRepository
from app.schemas.users import CreateUserDTO, UserInDBDTO, UserSuccesCreatedDTO


class MongoDBUserRepositoryImpl(UserRepository):
    def __init__(self, collection):
        self.collection = collection

    async def create(self, user_data: CreateUserDTO) -> UserSuccesCreatedDTO:
        raise NotImplementedError

    async def get_by_username(self, username: str) -> Optional[UserInDBDTO]:
        raise NotImplementedError
