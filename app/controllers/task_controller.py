from app.services.task_service import (
    TaskService
)


class TaskController:

    def __init__(
        self,
        task_service: TaskService
    ):
        self.task_service = task_service

    async def manage_task(
        self,
        request
    ):
        return await (
            self.task_service.manage_task(
                request
            )
        )

    async def get_tasks(
        self,
        user_id: int,
        task_id: int | None = None
    ):
        return await (
            self.task_service.get_tasks(
                user_id,
                task_id
            )
        )