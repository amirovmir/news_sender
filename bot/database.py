from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from bot.config import settings
from bot.models.user import Base, User, ChatHistory
from loguru import logger

engine = create_async_engine(settings.database_url, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(telegram_id: int, username: str | None) -> User:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            await session.flush()
            await session.refresh(user)
        return user


async def get_user(telegram_id: int) -> User | None:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def update_user_city(telegram_id: int, city_name: str, lat: float, lon: float):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(city_name=city_name, city_lat=lat, city_lon=lon)
        )


async def update_user_time(telegram_id: int, notification_time: str):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(notification_time=notification_time)
        )


async def toggle_user_active(telegram_id: int, is_active: bool):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_active=is_active)
        )


async def get_all_active_users() -> list[User]:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.is_active == True))
        return list(result.scalars().all())


async def add_chat_message(telegram_id: int, role: str, content: str):
    async with get_session() as session:
        msg = ChatHistory(user_id=telegram_id, role=role, content=content)
        session.add(msg)


async def get_chat_history(telegram_id: int, limit: int = 10) -> list[ChatHistory]:
    async with get_session() as session:
        result = await session.execute(
            select(ChatHistory)
            .where(ChatHistory.user_id == telegram_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))
