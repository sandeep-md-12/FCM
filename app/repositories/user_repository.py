from sqlalchemy import select

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def create(
        self,
        user: User
    ) -> User:

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user


    async def get_by_id(
        self,
        user_id: int
    ) -> User | None:

        stmt = (
            select(User)
            .where(
                User.id == user_id,
                User.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


    async def get_all(self):

        stmt = (
            select(User)
            .where(User.is_active.is_(True))
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()