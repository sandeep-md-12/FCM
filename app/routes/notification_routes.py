from fastapi import APIRouter, Depends

from app.controllers.notification_controller import (
    NotificationController
)


from app.schemas.notification import (
    RegisterTokenRequest,
    UnregisterTokenRequest,
    ReadNotificationRequest
)
from app.dependencies.services import (
    get_notification_service,
    get_device_token_service
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("")
async def get_notifications(
    user_id: int,
    notification_service=
    Depends(get_notification_service),

    token_service=
    Depends(get_device_token_service)
):

    controller = NotificationController(
        notification_service,
        token_service
    )

    return await (
        controller.get_notifications(
            user_id
        )
    )


@router.get("/unread-count")
async def unread_count(
    user_id: int,
    notification_service=
    Depends(get_notification_service),

    token_service=
    Depends(get_device_token_service)
):

    controller = NotificationController(
        notification_service,
        token_service
    )

    return await (
        controller.get_unread_count(
            user_id
        )
    )


@router.patch("/read")
async def read_notifications(
     request: ReadNotificationRequest,
    notification_service=
    Depends(get_notification_service),

    token_service=
    Depends(get_device_token_service)
):

    controller = NotificationController(
        notification_service,
        token_service
    )

    return await (
        controller.read_notifications(
            request
        )
    )



from app.schemas.notification import (
    RegisterTokenRequest
)
@router.post("/test")
async def test_notification(
    user_id: int,
    notification_service=Depends(get_notification_service)
):
    return await notification_service.send_test_notification(
        user_id=user_id
    )

@router.post("/register-token")
async def register_token(
    request: RegisterTokenRequest,
    notification_service=Depends(get_notification_service),
    token_service=Depends(get_device_token_service)
):
    controller = NotificationController(
        notification_service,
        token_service
    )

    return await controller.register_token(
        request
    )

@router.post("/unregister-token")
async def unregister_token(
    request: UnregisterTokenRequest,
    notification_service=
    Depends(get_notification_service),

    token_service=
    Depends(get_device_token_service)
):

    controller = NotificationController(
        notification_service,
        token_service
    )

    return await (
        controller.unregister_token(
            request
        )
    )