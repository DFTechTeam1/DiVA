from typing import Literal
from src.secret import Config
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

config = Config()


def database_connection(connection_type: Literal["sync", "async"] = "sync") -> AsyncEngine | Engine:
    if connection_type == "async":
        return create_async_engine(url=config.ASYNC_PGSQL_CONNECTION)
    return create_engine(url=config.SYNC_PGSQL_CONNECTION)


async def get_db() -> AsyncSession:
    async with database_connection(connection_type="async").connect() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
