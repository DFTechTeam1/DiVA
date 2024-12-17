from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field, Relationship
from services.postgres.connection import database_connection
from src.schema.request_format import ModelType


class CategoryDataDocumentation(SQLModel, table=True):
    __tablename__ = "category_documentation"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(unique=True)
    category: str = Field(default=None)
    description: str = Field(default=None)
    object_details: list["ObjectDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )
    environment_details: list["EnvironmentDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )
    design_type_details: list["DesignTypeDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )
    time_period_details: list["TimePeriodDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )
    dominant_color_details: list["DominantColorDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )
    culture_style_details: list["CultureStyleDocumentationDetails"] = Relationship(
        back_populates="information",
        cascade_delete=True,
    )


class ObjectDocumentationDetails(SQLModel, table=True):
    __tablename__ = "object_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="object_details"
    )


class EnvironmentDocumentationDetails(SQLModel, table=True):
    __tablename__ = "environment_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="environment_details"
    )


class DesignTypeDocumentationDetails(SQLModel, table=True):
    __tablename__ = "design_type_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="design_type_details"
    )


class TimePeriodDocumentationDetails(SQLModel, table=True):
    __tablename__ = "time_period_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="time_period_details"
    )


class DominantColorDocumentationDetails(SQLModel, table=True):
    __tablename__ = "dominant_color_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="dominant_color_details"
    )


class CultureStyleDocumentationDetails(SQLModel, table=True):
    __tablename__ = "culture_style_details"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="category_documentation.unique_id",
        ondelete="CASCADE",
    )
    category: str = Field(default=None)
    description: str = Field(default=None)
    information: CategoryDataDocumentation = Relationship(
        back_populates="culture_style_details"
    )


class ModelCard(SQLModel, table=True):
    __tablename__ = "model_card"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime = Field(default=None)
    started_task_at: datetime = Field(default=None)
    finished_task_at: datetime = Field(default=None)
    unique_id: str = Field(unique=True, default=None)
    model_name: str = Field(default=None)
    model_path: str = Field(default=None)
    model_type: ModelType = Field(default=None)
    trained_image: int = Field(default=None)
    model_details: list["ModelAccuracy"] = Relationship(
        back_populates="information", cascade_delete=True
    )


class ModelAccuracy(SQLModel, table=True):
    __tablename__ = "model_accuracy"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    unique_id: str = Field(
        foreign_key="model_card.unique_id",
        ondelete="CASCADE",
    )
    test_accuracy: int = Field(default=None)
    information: ModelCard = Relationship(back_populates="model_details")


class ImageTag(SQLModel, table=True):
    __tablename__ = "image_tag"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime = Field(default=None, nullable=True)
    filepath: str = Field(default=None)
    filename: str = Field(default=None)
    nature: bool = Field(default=False)
    artifacts: bool = Field(default=False)
    living_beings: bool = Field(default=False)
    natural: bool = Field(default=False)
    manmade: bool = Field(default=False)
    conceptual: bool = Field(default=False)
    art_deco: bool = Field(default=False)
    architectural: bool = Field(default=False)
    artistic: bool = Field(default=False)
    sci_fi: bool = Field(default=False)
    fantasy: bool = Field(default=False)
    day: bool = Field(default=False)
    afternoon: bool = Field(default=False)
    evening: bool = Field(default=False)
    night: bool = Field(default=False)
    dominant_colors: bool = Field(default=False)
    warm: bool = Field(default=False)
    cool: bool = Field(default=False)
    neutral: bool = Field(default=False)
    gold: bool = Field(default=False)
    asian: bool = Field(default=False)
    european: bool = Field(default=False)
    is_validated: bool = Field(default=False)
    ip_address: str = Field(default=None)


async def database_migration():
    engine = database_connection(connection_type="async")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
