from sqlalchemy import select

from app.repositories.base_repository import BaseRepository

from app.models.user_device_token import (
    UserDeviceToken
)


class UserDeviceTokenRepository(
    BaseRepository
):

    async def create(
        self,
        token: UserDeviceToken
    ):

        self.db.add(token)

        await self.db.commit()

        await self.db.refresh(token)

        return token

    async def update(
        self,
        token: UserDeviceToken
    ):

        await self.db.commit()

        await self.db.refresh(token)

        return token

    async def get_active_tokens(
        self,
        user_id: int
    ):

        stmt = (
            select(UserDeviceToken)
            .where(
                UserDeviceToken.user_id ==
                user_id,
                UserDeviceToken.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_by_token(
        self,
        fcm_token: str
    ):

        stmt = (
            select(UserDeviceToken)
            .where(
                UserDeviceToken.fcm_token ==
                fcm_token
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def deactivate(
        self,
        token: UserDeviceToken
    ):

        token.is_active = False

        await self.db.commit()

        await self.db.refresh(token)

        return token