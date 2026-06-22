import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from sqlalchemy.orm import DeclarativeBase


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/task_db"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def init_db():

    from app.models.user import User
    from app.models.task import Task
    from app.models.notification import Notification
    from app.models.user_notification import UserNotification
    from app.models.user_device_token import UserDeviceToken

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)