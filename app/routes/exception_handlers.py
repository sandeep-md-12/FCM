from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import (
    TaskNotFoundException,
    UserNotFoundException,
    NotificationNotFoundException
)

async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "message": "Task not found"
        }
    )


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "message": "User not found"
        }
    )


async def notification_not_found_handler(
    request: Request,
    exc: NotificationNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
            "Notification not found"
        }
    )