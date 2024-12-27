from sqlalchemy import insert, select, update
from services.postgres.connection import database_connection
from services.postgres.models import ModelCard
from utils.custom_errors import DatabaseQueryError, DataNotFoundError
from utils.logger import logging
from sqlalchemy.engine.row import Row
from utils.helper import local_time
from datetime import datetime
from typing import Literal


def insert_classification_model_card(
    started_task_at: datetime,
    finished_task_at: datetime,
    model_type: Literal["classification", "query"],
    model_name: str,
    model_path: str,
    trained_image: int,
    unique_id: str,
) -> None:
    with database_connection().connect() as session:
        try:
            query = insert(ModelCard).values(
                created_at=local_time(),
                started_task_at=started_task_at,
                finished_task_at=finished_task_at,
                unique_id=unique_id,
                model_path=model_path,
                model_name=model_name,
                model_type=model_type,
                trained_image=trained_image,
            )
            session.execute(query)
            session.commit()
            logging.info(
                f"[insert_classification_model_card] Inserted new {model_type} model card."
            )
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[insert_classification_model_card] Error inserting data: {e}"
            )
            session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            session.close()


def extract_models_card_entry(
    model_type: Literal["classification", "query"],
) -> Row:
    with database_connection().connect() as session:
        try:
            query = select(ModelCard).where(ModelCard.model_type == model_type)
            result = session.execute(query)
            entry = result.fetchone()
            return entry
        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[insert_classification_model_card] Error inserting data: {e}"
            )
            session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            session.close()


def update_model_card_entry(
    started_task_at: datetime,
    finished_task_at: datetime,
    model_type: Literal["classification", "query"],
    trained_image: int,
) -> None:
    with database_connection().connect() as session:
        try:
            query = (
                update(ModelCard)
                .where(ModelCard.model_type == model_type)
                .values(
                    started_task_at=started_task_at,
                    finished_task_at=finished_task_at,
                    trained_image=trained_image,
                )
            )
            session.execute(query)
            session.commit()
            logging.info(f"[update_model_card_entry] Updated {model_type} model card.")
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(f"[update_model_card_entry] Error inserting data: {e}")
            session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            session.close()
