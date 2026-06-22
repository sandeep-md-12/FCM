from datetime import datetime
from sqlalchemy import Index

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.utils.database import Base


class UserNotification(Base):
    __tablename__ = "user_notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notifications.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    notification = relationship(
        "Notification",
        back_populates="user_notifications"
    )

    user = relationship(
        "User",
        back_populates="user_notifications"
    )

    __table_args__ = (Index(
        "idx_user_notification_user",
        "user_id"
    ),
)

    def __eq__(self, other):
        return isinstance(other, UserNotification) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"UserNotification(id={self.id})"

    def __repr__(self):
        return self.__str__()