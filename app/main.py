from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes.user_routes import router as user_router
from app.routes.task_routes import router as task_router
from app.routes.notification_routes import router as notification_router

from app.utils.database import init_db
from app.utils.firebase import initialize_firebase
import os
from app.handlers.exception_handlers import (
    task_not_found_handler,
    user_not_found_handler,
    notification_not_found_handler
)

from app.utils.exceptions import (
    TaskNotFoundException,
    UserNotFoundException,
    NotificationNotFoundException
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    initialize_firebase()

    yield

app = FastAPI(
    title="Task Notification System",
    lifespan=lifespan
)

app.include_router(user_router)

app.include_router(task_router)

app.include_router(notification_router)


app.add_exception_handler(
    TaskNotFoundException,
    task_not_found_handler
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)

app.add_exception_handler(
    NotificationNotFoundException,
    notification_not_found_handler
)


@app.get("/test-fcm")
async def get_fcm_page():
    # Points to your templates folder
    file_path = os.path.join("templates", "index.html")
    return FileResponse(file_path)

# Route to serve the empty service worker (Crucial for FCM browser registration)
@app.get("/firebase-messaging-sw.js")
async def get_service_worker():
    file_path = os.path.join("templates", "firebase-messaging-sw.js")
    return FileResponse(file_path, media_type="application/javascript")