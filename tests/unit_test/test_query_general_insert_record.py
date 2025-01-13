import pytest
from uuid import uuid4
from faker import Faker
from services.postgres.connection import get_db
from utils.custom_error import DatabaseQueryError
from services.postgres.models import CategoryDataDocumentation
from utils.query.general import find_record, delete_record, insert_record


@pytest.mark.asyncio
async def test_insert_record_with_single_data():
    faker = Faker()
    unique_id = str(uuid4())
    category = faker.color_name()
    description = faker.name()
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": category, "description": description},
        )
        record = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        break

    assert record is not None
    assert type(record) is list
    assert len(record) == 1
    assert record[0]["unique_id"] == unique_id
    assert record[0]["category"] == category
    assert record[0]["description"] == description


@pytest.mark.asyncio
async def test_insert_record_with_multi_data():
    faker = Faker()
    records_to_insert = [
        {"unique_id": str(uuid4()), "category": faker.color_name(), "description": faker.name()},
        {"unique_id": str(uuid4()), "category": faker.color_name(), "description": faker.name()},
        {"unique_id": str(uuid4()), "category": faker.color_name(), "description": faker.name()},
    ]
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        for record in records_to_insert:
            await insert_record(db=db, table=CategoryDataDocumentation, data=record)
        all_record = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        break

    assert all_record is not None
    assert type(all_record) is list
    assert len(all_record) == len(records_to_insert)
    for i, record in enumerate(all_record):
        assert record["unique_id"] == records_to_insert[i]["unique_id"]
        assert record["category"] == records_to_insert[i]["category"]
        assert record["description"] == records_to_insert[i]["description"]


@pytest.mark.asyncio
async def test_insert_record_by_forcing_not_null_table():
    faker = Faker()
    unique_id = str(uuid4())
    category = faker.color_name()
    async for db in get_db():
        with pytest.raises(DatabaseQueryError, match="Database query error."):
            await delete_record(db=db, table=CategoryDataDocumentation)
            await insert_record(db=db, table=CategoryDataDocumentation, data={"unique_id": unique_id, "category": category})


@pytest.mark.asyncio
async def test_insert_record_with_large_data():
    faker = Faker()
    unique_id = str(uuid4())
    category = faker.color_name()
    description = "a" * 10000
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": category, "description": description},
        )
        record = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        break

    assert record is not None
    assert type(record) is list
    assert len(record) == 1
    assert record[0]["unique_id"] == unique_id
    assert record[0]["category"] == category
    assert record[0]["description"] == description


@pytest.mark.asyncio
async def test_insert_record_raised_value_error():
    async for db in get_db():
        with pytest.raises(ValueError):
            await insert_record(db=db, table=CategoryDataDocumentation, data={"invalid_column": "invalid_value"})


@pytest.mark.asyncio
async def test_insert_record_raised_exception_error():
    async for db in get_db():
        with pytest.raises(DatabaseQueryError, match="Database query error."):
            await insert_record(db=db, table=CategoryDataDocumentation, data={"unique_id": uuid4()})


@pytest.mark.asyncio
async def test_insert_record_with_empty_data():
    async for db in get_db():
        with pytest.raises(ValueError, match="Data must be a non-empty dictionary."):
            await insert_record(db=db, table=CategoryDataDocumentation, data={})
