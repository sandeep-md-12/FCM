from datetime import datetime

from app.models.notification import Notification
from app.models.user_notification import UserNotification

from app.utils.fcm import (
    send_to_multiple_tokens,
    is_invalid_token
)

from app.utils.exceptions import (
    NotificationNotFoundException
)
from app.tasks.notification_tasks import (
    send_notification_task
)


class NotificationService:

    def __init__(
        self,
        notification_repository,
        user_notification_repository,
        token_repository
    ):
        self.notification_repository = notification_repository
        self.user_notification_repository = user_notification_repository
        self.token_repository = token_repository

    async def send_task_status_notification(
        self,
        task,
        old_status: str,
        new_status: str,
        modified_by: int
    ):
        """
        Create notification record,
        create user notification mappings,
        send FCM notifications,
        cleanup invalid tokens.
        """

        message = (
            f"Task #{task.id} status changed "
            f"from {old_status} to {new_status}"
        )

        notification = Notification(
            title="Task Status Updated",
            message=message,
            task_id=task.id,
            old_status=old_status,
            new_status=new_status,
            created_by=modified_by
        )

        notification = await self.notification_repository.create(
            notification
        )

        recipient_ids = {
            task.user_id,
            task.created_by
        }

        for user_id in recipient_ids:

            user_notification = UserNotification(
                notification_id=notification.id,
                user_id=user_id
            )

            await self.user_notification_repository.create(
                user_notification
            )

            tokens = await self.token_repository.get_active_tokens(
                user_id
            )

            token_values = [
                token.fcm_token
                for token in tokens
            ]

            if not token_values:
                continue
            # this is for instant notification which runs along the fast API no scheduler delay
            # responses = await send_to_multiple_tokens(
            #     tokens=token_values,
            #     title="Task Status Updated",
            #     body=message
            # )

            #this block of code gets executed when we want to send notification with by using background task runner which is Celery (redis)
            # send_notification_task.delay(
            #     token_values,
            #     title="Task Status Updated",
            #     body=message
            # )

            ## this block of code is for timeout 

            print("SENDING TASK TO CELERY")

            
            result = send_notification_task.apply_async(
            args=[
                token_values
            ],
            kwargs={
                "title": "Task Status Updated",
                "body": message,
                "link": "https://github.com/"
            },
            countdown=10
        )
        print("TASK ID:", result.id)
            # for response in responses:

            #     if response["success"]:
            #         continue

            #     if is_invalid_token(
            #         response["error"]
            #     ):

            #         token = (
            #             await self.token_repository.get_by_token(
            #                 response["token"]
            #             )
            #         )

            #         if token:

            #             await self.token_repository.deactivate(
            #                 token
            #             )

    async def get_notifications(
        self,
        user_id: int
    ):
        """
        Get all notifications for a user.
        """

        return await (
            self.user_notification_repository
            .get_for_user(user_id)
        )

    async def get_unread_count(
        self,
        user_id: int
    ):
        """
        Get unread notification count.
        """

        return await (
            self.user_notification_repository
            .unread_count(user_id)
        )

    async def mark_read(
        self,
        notification_id: int,
        user_id: int
    ):
        """
        Mark a single notification as read.
        """

        user_notification = (
            await self.user_notification_repository
            .get_by_notification_and_user(
                notification_id=notification_id,
                user_id=user_id
            )
        )

        if not user_notification:
            raise NotificationNotFoundException()

        user_notification.is_read = True
        user_notification.read_at = datetime.utcnow()

        return await (
            self.user_notification_repository
            .mark_read(user_notification)
        )

    async def mark_all_read(
        self,
        user_id: int
    ):
        """
        Mark all notifications as read.
        """

        await (
            self.user_notification_repository
            .mark_all_read(user_id)
        )

        return {
            "message": (
                "All notifications marked as read"
            )
        }
    async def send_test_notification(
    self,
    user_id: int
):

        tokens = await self.token_repository.get_active_tokens(
            user_id
        )

        token_values = [
            token.fcm_token
            for token in tokens
        ]

        if not token_values:
            return {
                "message": "No active tokens found"
            }
        

        send_notification_task.delay(
        token_values,
        title="Test Notification",
        body="FCM integration working"
        )

        # responses = await send_to_multiple_tokens(
        #     tokens=token_values,
        #     title="Test Notification",
        #     body="FCM integration working"
        # )

        # return responses
        return "success"