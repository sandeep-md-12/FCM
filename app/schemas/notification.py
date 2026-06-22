from enum import Enum
from enum import Enum

from pydantic import BaseModel


class RegisterTokenRequest(BaseModel):
    user_id: int
    fcm_token: str


class UnregisterTokenRequest(BaseModel):
    fcm_token: str


class NotificationAction(str, Enum):
    READ_ONE = "READ_ONE"
    READ_ALL = "READ_ALL"


class ReadNotificationRequest(BaseModel):

    action: NotificationAction

    user_id: int

    notification_id: int | None = None

class NotificationAction(str, Enum):

    READ_ONE = "READ_ONE"

    READ_ALL = "READ_ALL"


from pydantic import (
    BaseModel,
    model_validator
)


class NotificationReadRequest(BaseModel):

    action: NotificationAction

    user_id: int

    notification_id: int | None = None

    @model_validator(mode="after")
    def validate_request(self):

        if (
            self.action ==
            NotificationAction.READ_ONE
        ):

            if not self.notification_id:
                raise ValueError(
                    "notification_id required"
                )

        return self
    

from datetime import datetime
from pydantic import ConfigDict

from pydantic import BaseModel


class RegisterTokenRequest(BaseModel):
    user_id: int
    fcm_token: str


class NotificationResponse(BaseModel):

    notification_id: int

    title: str

    message: str

    task_id: int

    old_status: str

    new_status: str

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UnreadCountResponse(BaseModel):

    count: int