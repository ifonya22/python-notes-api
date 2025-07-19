from abc import ABC, abstractmethod
from typing import Any, List, Optional

from app.schemas.users import CreateUserDTO, UserInDBDTO, UserSuccesCreatedDTO
from app.utils.fields import PyObjectId


class UserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserInDBDTO]:
        pass

    @abstractmethod
    async def create(self, user: CreateUserDTO) -> UserSuccesCreatedDTO:
        pass


class NoteRepository(ABC):
    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> List[dict]:
        pass

    @abstractmethod
    async def get_all(self) -> List[dict]:
        pass

    @abstractmethod
    async def get_by_note_id(self, note_id: PyObjectId) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_note_id_and_user_id(self, note_id: PyObjectId, user_id: int) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    async def create(self, note: dict) -> dict:
        pass

    @abstractmethod
    async def soft_delete(self, note_id: PyObjectId, user_id: int) -> bool:
        pass

    @abstractmethod
    async def restore(self, note_id: PyObjectId) -> bool:
        pass

    @abstractmethod
    async def update(self, note_id: PyObjectId, user_id: int, update_data: dict) -> bool:
        pass
