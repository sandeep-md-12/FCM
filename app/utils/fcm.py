from firebase_admin import messaging

from app.utils.exceptions import (
    FCMNotificationException
)


async def send_to_token(
    token: str,
    title: str,
    body: str
):

    try:

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )

        return messaging.send(message)

    except Exception as exc:
        raise FCMNotificationException(
            str(exc)
        )
    













    from firebase_admin import messaging


def send_to_multiple_tokens(
    tokens: list[str],
    title: str,
    body: str
):

    responses = []

    for token in tokens:

        try:

            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token
            )

            response = messaging.send(message)

            responses.append(
                {
                    "token": token,
                    "success": True,
                    "response": response
                }
            )

        except Exception as exc:

            responses.append(
                {
                    "token": token,
                    "success": False,
                    "error": str(exc)
                }
            )

    return responses

















from firebase_admin import messaging


def is_invalid_token(error_message: str):

    invalid_keywords = [
        "registration-token-not-registered",
        "unregistered",
        "sender-id-mismatch"
    ]

    error = error_message.lower()

    return any(
        keyword in error
        for keyword in invalid_keywords
    )