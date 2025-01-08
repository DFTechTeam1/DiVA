# import pytest
# from unittest import TestCase
# from unittest.mock import AsyncMock, patch
# from utils.query.general import find_record
# from services.postgres.connection import get_db
# from services.postgres.models import ImageTag
# from sqlmodel import SQLModel, Field

# class MockDB(TestCase):
#     async def session(self):
#         async for db in get_db():
#             return db
#         rows = await find_record(db)

# class MockTable(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name: str

# @pytest.mark.asyncio
# async def test_find_record_with_available_data():
#     # Use AsyncMock to simulate async db session
#     mock_db = AsyncMock()

#     # Simulate fetchall and fetchone to return expected results
#     mock_db.execute.return_value.fetchall = AsyncMock()
#     mock_db.execute.return_value.fetchone = AsyncMock()

#     mock_db.execute.return_value.fetchall.return_value = [
#         {"id": 1, "name": "test1"},
#         {"id": 2, "name": "test2"}
#     ]

#     mock_db.execute.return_value.fetchone.return_value = {"id": 1, "name": "test1"}

#     # Call the function under test
#     result = await find_record(db=mock_db, table=MockTable, fetch_type="all")
#     assert result == [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]

#     result = await find_record(db=mock_db, table=MockTable, fetch_type="one", id=1)
#     assert result == {"id": 1, "name": "test1"}

#     # Ensure session is closed properly
#     await mock_db.close.assert_awaited_once()
