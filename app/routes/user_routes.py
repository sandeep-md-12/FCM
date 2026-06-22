from fastapi import APIRouter, Depends

from app.controllers.user_controller import (
    UserController
)

from app.dependencies.services import (
    get_user_service
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
from app.schemas.user import (
    UserCreateRequest
)

@router.post("")
async def create_user(
    request: UserCreateRequest,
    service=Depends(get_user_service)
):
    controller = UserController(service)

    return await controller.create_user(
        request
    )


@router.get("")
async def get_users(
    service=Depends(get_user_service)
):
    controller = UserController(service)

    return await controller.get_users()