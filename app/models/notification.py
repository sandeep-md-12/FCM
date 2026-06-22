from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.utils.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    old_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    creator = relationship(
    "User"
    )
    task = relationship(
        "Task",
        back_populates="notifications"
    )

    user_notifications = relationship(
        "UserNotification",
        back_populates="notification"
    )

    def __eq__(self, other):
        return isinstance(other, Notification) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Notification(id={self.id})"

    def __repr__(self):
        return self.__str__()