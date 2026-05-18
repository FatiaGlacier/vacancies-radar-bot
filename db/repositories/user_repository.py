from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import User

async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )

    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, telegram_id: int) -> User:
    user = User(telegram_id=telegram_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user