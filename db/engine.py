from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import get_database_url
from db.models.user import User
from db.base import Base

engine = create_async_engine(get_database_url(), echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
