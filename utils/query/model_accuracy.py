from sqlalchemy import insert
from services.postgres.connection import database_connection
from services.postgres.models import ModelAccuracy
from utils.custom_errors import DatabaseQueryError
from utils.logger import logging
from utils.helper import local_time


def insert_test_accuracy(unique_id: str, test_accuracy: float) -> None:
    with database_connection().connect() as session:
        try:
            query = insert(ModelAccuracy).values(
                created_at=local_time(),
                unique_id=unique_id,
                test_accuracy=test_accuracy,
            )
            session.execute(query)
            session.commit()
            logging.info("[insert_test_accuracy] Inserted new test accuracy model.")
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(f"[insert_test_accuracy] Error inserting data: {e}")
            session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            session.close()
