import logging
from services.postgres.connection import database_connection
from utils.custom_errors import DatabaseQueryError, DataNotFoundError
from sqlmodel.main import SQLModelMetaclass
from sqlalchemy import select


async def retrieve_all(table_model: SQLModelMetaclass) -> list:
    """This function retrieves all entries from a database table using an asynchronous connection and
    returns them as a list of dictionaries.

    Parameters
    ----------
    table_model : SQLModelMetaclass
        The `table_model` parameter in the `retrieve_all` function is expected to be a class that
    represents a table in a SQL database. It is likely a SQLAlchemy model class that is defined using
    the `SQLModelMetaclass`. This class would typically have attributes that define the structure of the
    table,

    Returns
    -------
        The function `retrieve_all` is returning a list of dictionaries where each dictionary represents a
    row of data retrieved from the database table specified by the `table_model` parameter. Each
    dictionary contains key-value pairs where the keys are the column names of the table and the values
    are the corresponding data values for that row.

    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(table_model).order_by(table_model.id)
            result = await session.execute(query)
            rows = result.fetchall()

            if not rows:
                logging.error(
                    f"[retrieve_all] No data entry in table {table_model.__tablename__}!"
                )
                raise DataNotFoundError("Data entry not found.")

            logging.info(
                f"[table_model] Retrieve all data {table_model.__tablename__}."
            )
            return [dict(row._mapping) for row in rows]

        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(f"[retrieve_all] Error retrieving all entry: {e}")
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query.")
        finally:
            await session.close()


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
            query = select(table_model).exists().select()
            result = await session.execute(query)
            record = result.scalar()
            return record

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
