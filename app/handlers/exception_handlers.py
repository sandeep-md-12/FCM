from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import (
    TaskNotFoundException,
    UserNotFoundException,
    NotificationNotFoundException
)



async def task_not_found_handler(request: Request, exc: TaskNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail if hasattr(exc, 'detail') else "Task not found"}
    )

async def user_not_found_handler(request: Request, exc: UserNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail if hasattr(exc, 'detail') else "User not found"}
    )

async def notification_not_found_handler(request: Request, exc: NotificationNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail if hasattr(exc, 'detail') else "Notification not found"}
    )