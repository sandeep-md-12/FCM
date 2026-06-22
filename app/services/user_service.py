from app.models.user import User

from app.utils.exceptions import (
    UserNotFoundException
)


class UserService:

    def __init__(
        self,
        user_repository
    ):
        self.user_repository = user_repository

    async def create_user(
        self,
        username: str,
        email: str
    ):

        user = User(
            username=username,
            email=email
        )

        return await self.user_repository.create(
            user
        )

    async def get_user(
        self,
        user_id: int
    ):

        user = await self.user_repository.get_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundException()

        return user

    async def get_all_users(self):

        return await (
            self.user_repository.get_all()
        )