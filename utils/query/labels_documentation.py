from uuid import uuid4
from services.postgres.connection import database_connection
from utils.custom_errors import DatabaseQueryError
from sqlmodel.main import SQLModelMetaclass
from utils.logger import logging
from utils.helper import local_time
from sqlalchemy import insert, select


async def validate_data_availability(table_model: SQLModelMetaclass) -> bool:
    """
    This Python async function validates the availability of data in a database table using an
    SQLModelMetaclass object.

    :param table_model: The `table_model` parameter in the `validate_data_availability` function is
    expected to be a SQLAlchemy model class that represents a table in the database. This class should
    be a subclass of `SQLModelMetaclass`, which is likely a custom metaclass for SQLAlchemy models in
    your codebase. The
    :type table_model: SQLModelMetaclass
    :return: The function `validate_data_availability` returns a boolean value indicating whether the
    data represented by the `table_model` exists in the database. If the data exists, it returns `True`,
    otherwise it returns `False`.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(select(table_model).exists())
            result = await session.execute(query)
            return result.scalar()

        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return False


async def insert_category_documentation(
    table_model: SQLModelMetaclass, category: str, description: str
) -> str:
    """
    This async function inserts documentation for a category into a database table and returns the
    unique ID generated for the entry.

    :param table_model: The `table_model` parameter in the `insert_category_documentation` function is
    expected to be a SQLModelMetaclass object. This object likely represents a table in a database and
    is used to define the structure and properties of the table
    :type table_model: SQLModelMetaclass
    :param category: The `category` parameter in the `insert_category_documentation` function represents
    the category of the document being inserted into the database. It is a string that describes the
    category to which the document belongs. For example, if you are inserting a document related to
    "Technology", then "Technology" would be
    :type category: str
    :param description: The `insert_category_documentation` function is an asynchronous function that
    inserts a new category document into a database table using the provided `table_model`, `category`,
    and `description` parameters
    :type description: str
    :return: The function `insert_category_documentation` is returning the unique identifier
    (`unique_id`) of the inserted category documentation.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            unique_id = str(uuid4())
            query = insert(table_model).values(
                created_at=local_time(),
                unique_id=unique_id,
                category=category,
                description=description,
            )
            await session.execute(query)
            await session.commit()
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return unique_id


async def insert_details_documentation(
    table_model: SQLModelMetaclass, unique_id: str, category: str, description: str
) -> None:
    """
    This asynchronous function inserts details documentation into a database table using the provided
    parameters.

    :param table_model: The `table_model` parameter in the `insert_details_documentation` function is
    expected to be a SQLModelMetaclass object. This object likely represents a table in a database and
    is used to define the structure and properties of the table
    :type table_model: SQLModelMetaclass
    :param unique_id: The `unique_id` parameter in the `insert_details_documentation` function is a
    string that represents a unique identifier for the document being inserted into the database. It is
    used as a key to uniquely identify the document within the database table
    :type unique_id: str
    :param category: The `category` parameter in the `insert_details_documentation` function represents
    the category to which the details being inserted belong. It is a string that helps classify or
    categorize the information being stored in the database. For example, if you are inserting details
    about products, the category could be "electronics
    :type category: str
    :param description: The `insert_details_documentation` function is an asynchronous function that
    inserts details into a database table. The function takes the following parameters:
    :type description: str
    :return: The function `insert_details_documentation` is returning `None`.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = insert(table_model).values(
                created_at=local_time(),
                unique_id=unique_id,
                category=category,
                description=description,
            )
            await session.execute(query)
            await session.commit()
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return None
