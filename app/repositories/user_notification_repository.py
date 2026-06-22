from datetime import datetime

from sqlalchemy import (
    select,
    func,
    update
)

from app.repositories.base_repository import BaseRepository

from app.models.user_notification import (
    UserNotification
)

from app.models.notification import (
    Notification
)


class UserNotificationRepository(BaseRepository):

    async def create(
        self,
        user_notification: UserNotification
    ):

        self.db.add(user_notification)

        await self.db.commit()

        await self.db.refresh(user_notification)

        return user_notification

    async def get_for_user(
        self,
        user_id: int
    ):

        stmt = (
            select(
                UserNotification,
                Notification
            )
            .join(
                Notification,
                Notification.id ==
                UserNotification.notification_id
            )
            .where(
                UserNotification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
        )

        result = await self.db.execute(stmt)

        return result.all()

    async def unread_count(
        self,
        user_id: int
    ):

        stmt = (
            select(
                func.count(UserNotification.id)
            )
            .where(
                UserNotification.user_id == user_id,
                UserNotification.is_read.is_(False)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar() or 0

    async def get_by_notification_and_user(
        self,
        notification_id: int,
        user_id: int
    ):

        stmt = (
            select(UserNotification)
            .where(
                UserNotification.notification_id ==
                notification_id,
                UserNotification.user_id ==
                user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def mark_read(
        self,
        user_notification: UserNotification
    ):

        user_notification.is_read = True

        user_notification.read_at = (
            datetime.utcnow()
        )

        await self.db.commit()

        await self.db.refresh(
            user_notification
        )

        return user_notification

    async def mark_all_read(
        self,
        user_id: int
    ):

        stmt = (
            update(UserNotification)
            .where(
                UserNotification.user_id ==
                user_id,
                UserNotification.is_read.is_(False)
            )
            .values(
                is_read=True,
                read_at=datetime.utcnow()
            )
        )

        await self.db.execute(stmt)

        await self.db.commit()