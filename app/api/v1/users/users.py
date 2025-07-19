from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps import (
    UserInDBDTO,
    get_current_active_auth_user,
    get_sql_user_service,
    validate_auth_user,
)
from app.services.auth import utils as auth_utils
from app.services.users.users import UserService

from .schemas import CreateUserV1, RegisterResponseV1, TokenInfoV1, UserResponseV1

router = APIRouter()


@router.post("/login/", response_model=TokenInfoV1)
async def login_user_jwt(user: UserInDBDTO = Depends(validate_auth_user)):
    jwt_payload = {"sub": user.username}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfoV1(access_token=token, token_type="Bearer")


@router.post("/register", response_model=RegisterResponseV1)
async def register_new_user(
    request: CreateUserV1,
    # db_factory: RepositoryDBFactory = Depends(get_repository_db_factory),
    user_service: UserService = Depends(get_sql_user_service),
):
    return await user_service.register(user_data=request)


@router.get("/users/me/", response_model=UserResponseV1)
def auth_user_check_self_info(
    user: UserResponseV1 = Depends(get_current_active_auth_user),
):
    return user
