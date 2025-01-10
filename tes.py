from uuid import uuid4
from utils.query.general import find_record, delete_record, insert_record
from services.postgres.models import CategoryDataDocumentation
from services.postgres.connection import get_db
from faker import Faker
import asyncio


async def clear_category_data():
    faker = Faker()
    unique_id = str(uuid4())
    random_category = faker.century()
    random_desc = faker.address()

    async for db in get_db():
        await delete_record(db=db, table=CategoryDataDocumentation)
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={"unique_id": unique_id, "category": random_category, "description": random_desc},
        )

        record = await find_record(db=db, table=CategoryDataDocumentation, unique_id=unique_id)
        print(record)
        break


# Run the test
asyncio.run(clear_category_data())
