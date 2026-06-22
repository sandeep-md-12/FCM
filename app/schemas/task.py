from enum import Enum

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ManageTaskRequest(BaseModel):

    action: TaskAction

    task_id: Optional[int] = None

    task_description: Optional[str] = None

    duration: Optional[int] = None

    status: Optional[TaskStatus] = None

    user_id: Optional[int] = None

    created_by: Optional[int] = None

    modified_by: Optional[int] = None

    
class TaskAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator
)

from app.models.task import TaskStatus


class ManageTaskRequest(BaseModel):

    action: TaskAction

    task_id: int | None = None

    task_description: str | None = None

    duration: int | None = None

    status: TaskStatus | None = None

    user_id: int | None = None

    created_by: int | None = None

    modified_by: int | None = None

    @model_validator(mode="after")
    def validate_request(self):

        if self.action == TaskAction.CREATE:

            required = [
                self.task_description,
                self.duration,
                self.user_id,
                self.created_by
            ]

            if any(value is None for value in required):
                raise ValueError(
                    "Missing create fields"
                )

        if self.action in [
            TaskAction.UPDATE,
            TaskAction.DELETE
        ]:

            if not self.task_id:
                raise ValueError(
                    "task_id is required"
                )

        return self
    
class TaskResponse(BaseModel):

    id: int

    task_description: str

    duration: int

    status: TaskStatus

    user_id: int

    created_by: int

    modified_by: int | None

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class TaskQuery(BaseModel):

    user_id: int

    task_id: int | None = None