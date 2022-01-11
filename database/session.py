from typing import AsyncIterator

from core.config import SYNC_DATABASE_URI, ASYNC_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_engine(SYNC_DATABASE_URI, echo=True)
async_engine = create_async_engine(ASYNC_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)

session = async_session()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        async with session.begin():
            yield session
