import pytest
from utils.query.general import find_record
from services.postgres.models import CategoryDataDocumentation
from services.postgres.connection import get_db


@pytest.mark.asyncio
async def test_find_record_with_available_data():
    async for db in get_db():
        record = await find_record(db=db, table=CategoryDataDocumentation, fetch_type="all")
        print(record)
        break

    assert len(record) == 6
