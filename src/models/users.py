from enum import UNIQUE

from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import String


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=100))
    #username: Mapped[str] = mapped_column(String(50))