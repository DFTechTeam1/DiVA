import pytest
from sqlmodel import SQLModel, Field


class ExampleTable(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str


@pytest.fixture
def example_table():
    return ExampleTable
