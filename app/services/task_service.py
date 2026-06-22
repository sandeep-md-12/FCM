from app.models.task import Task

from app.schemas.task import (
    ManageTaskRequest,
    TaskAction
)

from app.utils.exceptions import (
    TaskNotFoundException
)


class TaskService:

    def __init__(
        self,
        task_repository,
        notification_service
    ):
        self.task_repository = task_repository
        self.notification_service = notification_service

    async def manage_task(
        self,
        request: ManageTaskRequest
    ):

        if request.action == TaskAction.CREATE:
            return await self.create_task(request)

        if request.action == TaskAction.UPDATE:
            return await self.update_task(request)

        if request.action == TaskAction.DELETE:
            return await self.delete_task(request)

        raise ValueError("Invalid Task Action")

    async def create_task(
        self,
        request: ManageTaskRequest
    ):

        task = Task(
            task_description=request.task_description,
            duration=request.duration,
            status=request.status,
            user_id=request.user_id,
            created_by=request.created_by,
            modified_by=request.created_by
        )

        return await self.task_repository.create(
            task
        )

    async def update_task(
        self,
        request: ManageTaskRequest
    ):

        task = await self.task_repository.get_by_id(
            request.task_id
        )

        if not task:
            raise TaskNotFoundException()

        old_status = task.status

        if request.task_description is not None:
            task.task_description = (
                request.task_description
            )

        if request.duration is not None:
            task.duration = request.duration

        if request.status is not None:
            task.status = request.status

        if request.modified_by is not None:
            task.modified_by = request.modified_by

        updated_task = await (
            self.task_repository.update(task)
        )

        if (
            request.status is not None
            and
            old_status != request.status
        ):

            await (
                self.notification_service
                .send_task_status_notification(
                    task=updated_task,
                    old_status=old_status.value,
                    new_status=request.status.value,
                    modified_by=request.modified_by
                )
            )

        return updated_task

    async def delete_task(
        self,
        request: ManageTaskRequest
    ):

        task = await self.task_repository.get_by_id(
            request.task_id
        )

        if not task:
            raise TaskNotFoundException()

        return await self.task_repository.soft_delete(
            task
        )

    async def get_tasks(
        self,
        user_id: int,
        task_id: int | None = None
    ):

        if task_id:

            task = await (
                self.task_repository.get_by_id(
                    task_id
                )
            )

            if not task:
                raise TaskNotFoundException()

            return task

        return await (
            self.task_repository.get_by_user(
                user_id
            )
        )