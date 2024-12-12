from sqlalchemy import MetaData
from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field
from services.postgres.connection import database_connection

class ModelCard(SQLModel, table=True):
    __tablename__="model_card"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    started_task_at: datetime | None = Field(default=None)
    finished_task_at: datetime | None = Field(default=None)
    unique_id: str = Field(unique=True)
    model_name: str = Field(default=None)
    trained_image: int = Field(default=None)


async def database_migration():
    engine = database_connection(connection_type="async")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)