from enum import Enum

from app.api.deps import role_required


class Roles(Enum):
    ALL_ROLES = role_required("user", "admin")
    ADMIN_ONLY = role_required("admin")
    USER_ONLY = role_required("user")
