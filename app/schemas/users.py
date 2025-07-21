from dataclasses import dataclass


@dataclass
class UserInDBDTO:
    id: int
    username: str
    password: bytes
    role: str
    is_active: bool


@dataclass
class CreateUserDTO:
    username: str
    password: bytes

    role: str = "user"
    is_active: bool = True


@dataclass
class UserSuccesCreatedDTO:
    id: int
    username: str
    role: str
    is_active: bool
