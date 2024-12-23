from typing import Literal
from src.secret import Config
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

config = Config()


def database_connection(
    connection_type: Literal["sync", "async"] = "sync",
) -> AsyncEngine | Engine:
    """The function `database_connection` creates and returns either a synchronous or asynchronous database
    engine based on the specified connection type.

    Parameters
    ----------
    connection_type : Literal["sync", "async"], optional
        The `connection_type` parameter specifies the type of database connection to establish. It can have
    two possible values: "sync" for synchronous connection or "async" for asynchronous connection.

    Returns
    -------
        The function `database_connection` returns either an `AsyncEngine` object if the `connection_type`
    is set to "async", or an `Engine` object if the `connection_type` is set to "sync".

    """
    if connection_type == "async":
        return create_async_engine(url=config.ASYNC_PGSQL_CONNECTION)
    return create_engine(url=config.SYNC_PGSQL_CONNECTION, pool_pre_ping=True)
