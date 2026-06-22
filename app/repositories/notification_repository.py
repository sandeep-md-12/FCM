from sqlalchemy import select

from app.repositories.base_repository import BaseRepository

from app.models.notification import (
    Notification
)


class NotificationRepository(BaseRepository):

    async def create(
        self,
        notification: Notification
    ):

        self.db.add(notification)

        await self.db.commit()

        await self.db.refresh(notification)

        return notification

    async def get_by_id(
        self,
        notification_id: int
    ):

        stmt = (
            select(Notification)
            .where(
                Notification.id ==
                notification_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()