import pytest
from sqlmodel import SQLModel, Field
from uuid import uuid4
from faker import Faker
from sqlalchemy.engine.row import Row
from services.postgres.connection import get_db
from utils.custom_error import DatabaseQueryError
from services.postgres.models import CategoryDataDocumentation
from utils.query.general import find_record, delete_record, insert_record, update_record


class NonExistentTable(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category: str = Field(default=None)


# @pytest.mark.asyncio
# async def test_update_record_with_empty_data_inside_table():
#     async for db in get_db():
#         with pytest.raises(DataNotFoundError, match="Data not found"):
#             await update_record(
#                 db=db,
#                 table=CategoryDataDocumentation,
#                 conditions={"id": str(uuid4())},
#                 data={"category": "NonExistentCategory"}
#             )


@pytest.mark.asyncio
async def test_update_record_with_available_data():
    faker = Faker()
    unique_id = str(uuid4())
    old_category = faker.color_name()
    new_category = faker.color_name()
    old_desc = faker.address()
    new_desc = faker.address()
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": old_category, "description": old_desc},
        )
        await update_record(
            db=db,
            table=CategoryDataDocumentation,
            conditions={"unique_id": unique_id},
            data={"category": new_category, "description": new_desc},
        )
        updated_record = await find_record(db=db, table=CategoryDataDocumentation, unique_id=unique_id)

    assert updated_record is not None
    assert type(updated_record) is Row
    assert updated_record.category == new_category
    assert updated_record.description == new_desc


@pytest.mark.asyncio
async def test_update_record_with_empty_conditions():
    """Test updating a record with empty conditions."""
    faker = Faker()
    async for db in get_db():
        with pytest.raises(ValueError, match="Conditions cannot be empty"):
            await update_record(db=db, table=CategoryDataDocumentation, conditions={}, data={"category": faker.color_name()})


@pytest.mark.asyncio
async def test_update_record_with_empty_data_payload():
    """Test updating a record with empty conditions."""
    faker = Faker()
    unique_id = str(uuid4())
    old_category = faker.color_name()
    old_desc = faker.address()
    async for db in get_db():
        with pytest.raises(ValueError, match="Data must be a non-empty dictionary."):
            await insert_record(
                db=db,
                table=CategoryDataDocumentation,
                data={"unique_id": unique_id, "category": old_category, "description": old_desc},
            )
            await update_record(db=db, table=CategoryDataDocumentation, conditions={"unique_id": unique_id}, data={})


@pytest.mark.asyncio
async def test_update_record_raised_value_error():
    async for db in get_db():
        with pytest.raises(ValueError):
            await update_record(
                db=db,
                table=CategoryDataDocumentation,
                conditions={"unique_id": str(uuid4())},
                data={"invalid_column": "invalid_value"},
            )


@pytest.mark.asyncio
async def test_update_record_raised_exception_error():
    faker = Faker()
    async for db in get_db():
        with pytest.raises(DatabaseQueryError):
            await update_record(
                db=db, table=CategoryDataDocumentation, conditions={"unique_id": uuid4()}, data={"category": faker.address()}
            )


@pytest.mark.asyncio
async def test_update_record_with_nonexistent_table():
    """Test updating a record in a non-existent table."""
    async for db in get_db():
        with pytest.raises(DatabaseQueryError, match="Table does not exist."):
            await update_record(
                db=db, table=NonExistentTable, conditions={"id": str(uuid4())}, data={"category": "NonExistentCategory"}
            )
