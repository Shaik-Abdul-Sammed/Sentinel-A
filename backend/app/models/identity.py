from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class RoleORM(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, index=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    users = relationship("UserORM", back_populates="role_ref")


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    role_ref = relationship("RoleORM", back_populates="users")
