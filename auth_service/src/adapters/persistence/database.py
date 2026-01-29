from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# TODO: CHANGE TO K8S SECRET
SQLALCHEMY_DATABASE_URL = "cockroachdb+asyncpg://user:password@localhost:26257/auth_db"


class DatabaseConfig:
    def __init__(self, database_url: str = SQLALCHEMY_DATABASE_URL):
        self.engine = create_async_engine(
            database_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=0,
        )

        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session

    async def close(self) -> None:
        await self.engine.dispose()

    async def create_tables(self) -> None:
        from auth_service.src.adapters.persistence.models._sqlalchemy.base import Base

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
