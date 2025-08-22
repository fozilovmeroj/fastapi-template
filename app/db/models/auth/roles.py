from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm.attributes import Mapped

from app.db.base_models import WithTimeStamp, int_pk, Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int_pk]
    name: Mapped[str]

    roles: Mapped[list["Role"]] = relationship(secondary="role_permission", back_populates="permissions")


class Role(WithTimeStamp):
    __tablename__ = "roles"

    id: Mapped[int_pk]
    name: Mapped[str]

    permissions: Mapped[list["Permission"]] = relationship(secondary="role_permission", back_populates="roles")

class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)