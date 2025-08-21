from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from app.db.base_models import WithTimeStamp, int_pk, Base

role_permissions_table = Table(
    "role_permission",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int_pk]
    name: Mapped[str]

    roles: Mapped[list["Role"]] = relationship(secondary=role_permissions_table, back_populates="permissions")


class Role(WithTimeStamp):
    __tablename__ = "roles"

    id: Mapped[int_pk]
    name: Mapped[str]

    permissions: Mapped[list["Permission"]] = relationship(secondary=role_permissions_table, back_populates="roles")