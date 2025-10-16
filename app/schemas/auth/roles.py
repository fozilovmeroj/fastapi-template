from app.schemas.base import DBModel


class PermissionSchema(DBModel):
    id: int
    name: str


class RoleSchema(DBModel):
    id: int
    name: str


class RoleWithPermissionsSchema(RoleSchema):
    permissions: list[PermissionSchema]


class RoleCreateUpdate(DBModel):
    name: str
    permissions: list[int]
