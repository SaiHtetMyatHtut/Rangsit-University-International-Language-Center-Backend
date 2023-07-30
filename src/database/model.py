from datetime import datetime
from sqlalchemy import Boolean, Column, Table, Integer, String, DateTime, ForeignKey, UniqueConstraint, Enum
from src.database.setup import Base
from sqlalchemy.orm import relationship
import enum
# from sqlalchemy.dialects.postgresql import ENUM


class Route(enum.Enum):
    user = "user"


class Access(enum.Enum):
    read = "read"
    write = "write"
    full = "full"


roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
    UniqueConstraint("role_id", "permission_id", name="uix_1")
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    image_url = Column(String, nullable=True, default=None)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    role_id = Column(ForeignKey("roles.id"), nullable=False)

    roles = relationship("Role", back_populates="users")

    def repr(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, hashed_password={self.hashed_password}, image_url={self.image_url}, role={self.role})"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())

    users = relationship("User", back_populates="roles")
    permissions = relationship(
        "Permission", secondary=roles_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    route = Column(Enum(Route), index=True)
    access = Column(Enum(Access), index=True)
    created_at = Column(DateTime, default=datetime.utcnow())

    roles = relationship("Role", secondary=roles_permissions,
                         back_populates="permissions")


class Peer(Base):
    __tablename__ = "peers"

    __table_args__ = (
        UniqueConstraint("student_id", "mentor_id"),
    )

    student_id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    timestamp = Column(String, nullable=False)

    sections = relationship("Section", back_populates="peers")

    def repr(self):
        return f"Peer(sid={self.sid}, mid={self.mid}, timestamp={self.timestamp})"


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    end_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow())
    end_time = Column(DateTime, nullable=False, default=datetime.utcnow())

    peers = relationship("Peer", back_populates="sections")

    def repr(self):
        return f"Section(id={self.id}, name={self.name}, datetime={self.datetime})"
