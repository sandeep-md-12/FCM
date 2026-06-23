import asyncio

from app.utils.celery_app import (
    celery_app
)

from app.utils.fcm import (
    send_to_multiple_tokens
)

from app.utils.firebase import (
    initialize_firebase
)

initialize_firebase()



@celery_app.task(name="app.tasks.notification_tasks.send_notification_task")
def send_notification_task(
    tokens: list[str],
    title: str,
    body: str,
    link: str | None = None,
):
    print("TASK STARTED")

    responses = send_to_multiple_tokens(
        tokens=tokens,
        title=title,
        body=body,
        link=link or ""
    )

    print("FCM Responses:", responses)

    return responses