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



@celery_app.task
def send_notification_task(
    tokens: list[str],
    title: str,
    body: str
):
    print("TASK STARTED")

    responses = send_to_multiple_tokens(
        tokens=tokens,
        title=title,
        body=body
    )

    print("FCM Responses:", responses)

    return responses