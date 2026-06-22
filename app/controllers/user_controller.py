from app.services.user_service import (
    UserService
)


class UserController:

    def __init__(
        self,
        user_service: UserService
    ):
        self.user_service = user_service

    async def create_user(
        self,
        request
    ):
        return await self.user_service.create_user(
            username=request.username,
            email=request.email
        )

    async def get_users(self):
        return await (
            self.user_service.get_all_users()
        )