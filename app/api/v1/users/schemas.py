from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class CreateUserV1(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(8)]


class UserResponseV1(BaseModel):
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RegisterResponseV1(UserResponseV1):
    id: int


class TokenInfoV1(BaseModel):
    access_token: str
    token_type: str
