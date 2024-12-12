from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field, Relationship
from services.postgres.connection import database_connection

class DataSource(SQLModel, table=True):
    __tablename__ = "data_source"
    id: int = Field(primary_key=True)
    model_card_unique_id: str = Field(foreign_key="model_card.unique_id")
    source_name: str = Field(index=True, default=None)
    added_at: datetime = Field(default=local_time())
    model_card: list["ModelCard"] = Relationship(back_populates="data_sources")

class ModelCard(SQLModel, table=True):
    __tablename__ = "model_card"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    started_task_at: datetime | None = Field(default=None)
    finished_task_at: datetime | None = Field(default=None)
    unique_id: str = Field(unique=True, default=None)
    model_name: str = Field(default=None)
    trained_image: int = Field(default=None)
    data_sources: list[DataSource] = Relationship(back_populates="model_card")


async def database_migration():
    engine = database_connection(connection_type="async")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)