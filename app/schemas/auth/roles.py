from app.schemas.base import DBModel


class PermissionSchema(DBModel):
    id: int
    name: str


class RoleSchema(DBModel):
    id: int
    name: str
    permissions: list[PermissionSchema]
