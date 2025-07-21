from typing import Optional

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models.sql.user import Role, User
from app.database.repositories.base import UserRepository
from app.exceptions import UserAlreadyExistExc
from app.schemas.users import CreateUserDTO, UserInDBDTO, UserSuccesCreatedDTO


class SQLUserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[UserInDBDTO]:
        result = await self.session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            return None

        role: Optional[Role] = await self.session.get(Role, user.role_id)
        if not role:
            return None

        return UserInDBDTO(
            id=user.id,
            username=user.username,
            password=user.password,
            role=role.name,
            is_active=user.is_active,
        )

    async def create(self, user_data: CreateUserDTO) -> UserSuccesCreatedDTO:
        try:
            db_user = User(
                username=user_data.username,
                password=user_data.password,
                role_id=1,
                is_active=user_data.is_active,
            )

            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            role = await self.session.get(Role, db_user.role_id)
            if not role:
                raise ValueError("Role not found for existing user")
            return UserSuccesCreatedDTO(
                id=db_user.id,
                username=db_user.username,
                role=role.name,
                is_active=db_user.is_active,
            )
        except IntegrityError:
            await self.session.rollback()
            result = await self.session.execute(select(User).where(User.username == user_data.username))
            existing_user = result.scalars().first()
            if not existing_user:
                raise ValueError("User does not exist and could not be created")

            role = await self.session.get(Role, existing_user.role_id)
            if not role:
                raise ValueError("Role not found for existing user")

            raise UserAlreadyExistExc

    async def set_user_role(self, username: str, role_name: str) -> int:
        result = await self.session.execute(select(Role).where(Role.name == role_name))
        role = result.scalars().first()
        if not role:
            raise ValueError(f"Role '{role_name}' not found")

        stmt = update(User).where(User.username == username).values(role_id=role.id)
        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            await self.session.rollback()
            return 0

        await self.session.commit()
        return role.name
