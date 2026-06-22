from datetime import datetime
from sqlalchemy import Index

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.utils.database import Base


class UserDeviceToken(Base):
    __tablename__ = "user_device_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    fcm_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    user = relationship(
        "User",
        back_populates="device_tokens"
    )
    __table_args__ = (Index(
        "idx_user_token_user",
        "user_id"
    ),
)

    def __eq__(self, other):
        return isinstance(other, UserDeviceToken) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"UserDeviceToken(id={self.id})"

    def __repr__(self):
        return self.__str__()