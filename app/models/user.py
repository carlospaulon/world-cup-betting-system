import uuid
from datetime import datetime, date
from sqlalchemy import Uuid
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import Boolean
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True) # Unique?
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date] = mapped_column()
    points: Mapped[int] = mapped_column(default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) # server default, ensure that we have the exacly registry of the timestamp


    def __repr__(self):
        return f'User: {self.id}, name={self.nickname}'