from datetime import datetime
from enum import Enum
from sqlalchemy import Index


from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.utils.database import Base


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    task_description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    modified_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
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

    owner = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="owned_tasks"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks"
    )

    modifier = relationship(
        "User",
        foreign_keys=[modified_by],
        back_populates="modified_tasks"
    )

    notifications = relationship(
        "Notification",
        back_populates="task"
    )
    __table_args__ = (
    Index(
        "idx_task_user",
        "user_id"
    ),
)

    @property
    def task_duration(self):
        return self.duration

    @task_duration.setter
    def task_duration(self, value):
        if value < 0:
            raise ValueError("Duration cannot be negative")
        self.duration = value

    def __eq__(self, other):
        return isinstance(other, Task) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Task(id={self.id}, status={self.status})"

    def __repr__(self):
        return self.__str__()