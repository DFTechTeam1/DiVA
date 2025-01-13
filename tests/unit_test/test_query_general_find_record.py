import pytest
from uuid import uuid4
from faker import Faker
from sqlalchemy.engine.row import Row
from services.postgres.connection import get_db
from utils.custom_error import DatabaseQueryError
from services.postgres.models import CategoryDataDocumentation
from utils.query.general import find_record, delete_record, insert_record


@pytest.mark.asyncio
async def test_find_all_record_with_available_data():
    faker = Faker()
    records_to_insert = [
        {"unique_id": str(uuid4()), "category": faker.century(), "description": faker.name()},
        {"unique_id": str(uuid4()), "category": faker.color_name(), "description": faker.name()},
    ]

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        for record in records_to_insert:
            await insert_record(db=db, table=CategoryDataDocumentation, data=record)

        records = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        break

    assert len(records) == len(records_to_insert)
    assert type(records) is list
    for i, record in enumerate(records):
        assert record["unique_id"] == records_to_insert[i]["unique_id"]
        assert record["category"] == records_to_insert[i]["category"]
        assert record["description"] == records_to_insert[i]["description"]


@pytest.mark.asyncio
async def test_find_all_record_with_empty_data():
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        record = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        break

    assert record is None


@pytest.mark.asyncio
async def test_find_single_record_with_empty_data():
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        record = await find_record(db=db, table=CategoryDataDocumentation)
        break

    assert record is None


@pytest.mark.asyncio
async def test_find_single_record_with_available_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": random_category, "description": random_desc},
        )

        record = await find_record(db=db, table=CategoryDataDocumentation)
        break

    assert len([record]) == 1
    assert type(record) is Row
    assert record.unique_id == unique_id
    assert record.category == random_category
    assert record.description == random_desc


@pytest.mark.asyncio
async def test_find_record_by_unique_id_with_available_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": random_category, "description": random_desc},
        )

        record = await find_record(db=db, table=CategoryDataDocumentation, unique_id=unique_id)
        break

    assert record is not None
    assert type(record) is Row
    assert record.unique_id == unique_id
    assert record.category == random_category
    assert record.description == random_desc


@pytest.mark.asyncio
async def test_find_record_by_unique_id_with_empty_data():
    unique_id = str(uuid4())
    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        record = await find_record(db=db, table=CategoryDataDocumentation, unique_id=unique_id)
        break

    assert record is None


@pytest.mark.asyncio
async def test_find_record_by_category_with_available_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": random_category, "description": random_desc},
        )

        record = await find_record(db=db, table=CategoryDataDocumentation, category=random_category)
        break

    assert record is not None
    assert type(record) is Row
    assert record.unique_id == unique_id
    assert record.category == random_category
    assert record.description == random_desc


@pytest.mark.asyncio
async def test_find_record_by_description_with_empty_data():
    faker = Faker()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        record = await find_record(db=db, table=CategoryDataDocumentation, description=random_desc)
        break

    assert record is None


@pytest.mark.asyncio
async def test_find_record_using_multiple_filter_with_available_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": random_category, "description": random_desc},
        )

        record = await find_record(
            db=db,
            table=CategoryDataDocumentation,
            category=random_category,
            unique_id=unique_id,
            description=random_desc,
            fetch_type="all",
        )
        break

    assert record is not None
    assert type(record) is list
    assert record[0]["unique_id"] == unique_id
    assert record[0]["category"] == random_category
    assert record[0]["description"] == random_desc


@pytest.mark.asyncio
async def test_find_record_using_multiple_filter_with_empty_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.name()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        record = await find_record(
            db=db, table=CategoryDataDocumentation, category=random_category, unique_id=unique_id, description=random_desc
        )
        break

    assert record is None


@pytest.mark.asyncio
async def test_find_record_raised_value_error():
    async for db in get_db():
        with pytest.raises(ValueError):
            await find_record(db=db, table=CategoryDataDocumentation, invalid_column="invalid_value")
        break


@pytest.mark.asyncio
async def test_find_record_raised_exception_error():
    unique_id = uuid4()
    async for db in get_db():
        with pytest.raises(DatabaseQueryError):
            await find_record(db=db, table=CategoryDataDocumentation, unique_id=unique_id)
        break
