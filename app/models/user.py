from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    modified_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    owned_tasks = relationship(
        "Task",
        foreign_keys="Task.user_id",
        back_populates="owner"
    )

    created_tasks = relationship(
        "Task",
        foreign_keys="Task.created_by",
        back_populates="creator"
    )

    modified_tasks = relationship(
        "Task",
        foreign_keys="Task.modified_by",
        back_populates="modifier"
    )

    device_tokens = relationship(
        "UserDeviceToken",
        back_populates="user"
    )

    user_notifications = relationship(
        "UserNotification",
        back_populates="user"
    )

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"User(id={self.id}, username={self.username})"

    def __repr__(self):
        return self.__str__()