from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_notification_repository import UserNotificationRepository
from app.repositories.user_device_token_repository import UserDeviceTokenRepository

from app.services.user_service import UserService
from app.services.task_service import TaskService
from app.services.notification_service import NotificationService
from app.services.device_token_service import DeviceTokenService



def get_user_service(
    db: AsyncSession = Depends(get_db)
):

    user_repository = UserRepository(db)

    return UserService(
        user_repository=user_repository
    )


def get_notification_service(
    db: AsyncSession = Depends(get_db)
):

    notification_repository = NotificationRepository(db)

    user_notification_repository = (
        UserNotificationRepository(db)
    )

    token_repository = (
        UserDeviceTokenRepository(db)
    )

    return NotificationService(
        notification_repository=
        notification_repository,

        user_notification_repository=
        user_notification_repository,

        token_repository=
        token_repository
    )

def get_task_service(
    db: AsyncSession = Depends(get_db)
):

    from app.repositories.task_repository import TaskRepository
    task_repository = TaskRepository(db)

    notification_service = (
        get_notification_service(db)
    )

    return TaskService(
        task_repository=task_repository,
        notification_service=
        notification_service
    )

def get_device_token_service(
    db: AsyncSession = Depends(get_db)
):

    token_repository = (
        UserDeviceTokenRepository(db)
    )

    return DeviceTokenService(
        token_repository=token_repository
    )