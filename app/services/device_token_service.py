from datetime import datetime

from app.models.user_device_token import (
    UserDeviceToken
)


class DeviceTokenService:

    def __init__(
        self,
        token_repository
    ):
        self.token_repository = (
            token_repository
        )

    async def register_token(
        self,
        user_id: int,
        fcm_token: str
    ):

        existing = (
            await self.token_repository
            .get_by_token(fcm_token)
        )

        if existing:

            existing.is_active = True

            existing.last_seen = (
                datetime.utcnow()
            )

            return await (
                self.token_repository.update(
                    existing
                )
            )

        token = UserDeviceToken(
            user_id=user_id,
            fcm_token=fcm_token
        )

        return await (
            self.token_repository.create(
                token
            )
        )

    async def unregister_token(
        self,
        fcm_token: str
    ):

        token = (
            await self.token_repository
            .get_by_token(fcm_token)
        )

        if not token:
            return

        return await (
            self.token_repository.deactivate(
                token
            )
        )