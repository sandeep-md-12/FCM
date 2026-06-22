from sqlalchemy import select

from app.models.task import Task

from app.repositories.base_repository import BaseRepository



class TaskRepository(
    BaseRepository):
    async def create(
        self,
        task: Task
    ) -> Task:

        self.db.add(task)

        await self.db.commit()

        await self.db.refresh(task)

        return task

    async def get_by_id(
        self,
        task_id: int
    ) -> Task | None:

        stmt = (
            select(Task)
            .where(
                Task.id == task_id,
                Task.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: int
    ):

        stmt = (
            select(Task)
            .where(
                Task.user_id == user_id,
                Task.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def update(
        self,
        task: Task
    ):

        await self.db.commit()

        await self.db.refresh(task)

        return task

    async def soft_delete(
        self,
        task: Task
    ):

        task.is_active = False

        await self.db.commit()

        return task