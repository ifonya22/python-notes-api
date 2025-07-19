from fastapi import APIRouter

from app.api.v1.notes.notes_admin import router as notes_admin_v1_router
from app.api.v1.notes.notes_common_user import router as notes_common_user_v1_router
from app.api.v1.users.users import router as users_v1_router

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(notes_common_user_v1_router, prefix="/note", tags=["notes-user"])
api_router_v1.include_router(notes_admin_v1_router, prefix="/admin/note", tags=["notes-admin"])
api_router_v1.include_router(users_v1_router, prefix="/user", tags=["users"])
