from fastapi import APIRouter, Depends

from app.controllers.task_controller import (
    TaskController
)

from app.dependencies.services import (
    get_task_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

from app.schemas.task import (
    ManageTaskRequest
)

@router.post("/manage")
async def manage_task(
    request: ManageTaskRequest,
    service=Depends(get_task_service)
):
    controller = TaskController(service)

    return await controller.manage_task(
        request
    )


@router.get("")
async def get_tasks(
    user_id: int,
    task_id: int | None = None,
    service=Depends(get_task_service)
):
    controller = TaskController(service)

    return await controller.get_tasks(
        user_id,
        task_id
    )