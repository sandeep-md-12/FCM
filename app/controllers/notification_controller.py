from app.services.notification_service import (
    NotificationService
)

from app.services.device_token_service import (
    DeviceTokenService
)

from app.schemas.notification import (
    NotificationAction
)

class NotificationController:

    def __init__(
        self,
        notification_service,
        device_token_service
    ):
        self.notification_service = (
            notification_service
        )

        self.device_token_service = (
            device_token_service
        )

    async def get_notifications(
        self,
        user_id: int
    ):
        return await (
            self.notification_service
            .get_notifications(user_id)
        )

    async def get_unread_count(
        self,
        user_id: int
    ):
        return await (
            self.notification_service
            .get_unread_count(user_id)
        )

    async def read_notifications(
        self,
        request
    ):

        if (
            request.action ==
            NotificationAction.READ_ONE
        ):

            return await (
                self.notification_service
                .mark_read(
                    request.notification_id,
                    request.user_id
                )
            )

        return await (
            self.notification_service
            .mark_all_read(
                request.user_id
            )
        )

    async def register_token(
        self,
        request
    ):
        return await (
            self.device_token_service
            .register_token(
                request.user_id,
                request.fcm_token
            )
        )

    async def unregister_token(
        self,
        request
    ):
        return await (
            self.device_token_service
            .unregister_token(
                request.fcm_token
            )
        )