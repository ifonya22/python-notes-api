from dataclasses import dataclass

from app.api.deps import role_required


@dataclass
class Roles:
    ALL_ROLES = role_required("user", "admin")
    ADMIN_ONLY = role_required("admin")
    USER_ONLY = role_required("user")
