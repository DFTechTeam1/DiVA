from sqlalchemy import insert, select, update
from services.postgres.connection import database_connection
from services.postgres.models import ModelCard
from utils.custom_errors import DatabaseQueryError, DataNotFoundError
from utils.logger import logging
from sqlalchemy.engine.row import Row
from utils.helper import local_time
from datetime import datetime
from typing import Literal


async def insert_classification_model_card(
    started_task_at: datetime,
    finished_task_at: datetime,
    model_type: Literal["classification", "query"],
    model_name: str,
    trained_image: int,
    unique_id: str,
) -> None:
    """
    This async function inserts a classification or query model card into a database with specified
    details and handles potential errors.

    :param started_task_at: `started_task_at` is a datetime indicating when the task for the model
    started
    :type started_task_at: datetime
    :param finished_task_at: `finished_task_at` is a parameter representing the datetime when a task or
    process associated with a classification or query model is completed. It is used in the function
    `insert_classification_model_card` to record the timestamp when the task finishes
    :type finished_task_at: datetime
    :param model_type: The `model_type` parameter in the `insert_classification_model_card` function is
    a string literal that can only have one of two values: "classification" or "query". This parameter
    specifies the type of the model being inserted into the database, indicating whether it is a
    classification model or a query model
    :type model_type: Literal["classification", "query"]
    :param model_name: The `model_name` parameter in the `insert_classification_model_card` function
    represents the name of the classification or query model being inserted into the database. It is a
    string type parameter where you would provide the name of the model being stored in the database
    :type model_name: str
    :param trained_image: The `trained_image` parameter in the `insert_classification_model_card`
    function represents the number of images used to train the classification model. It is an integer
    value that indicates the size of the training dataset used for training the model
    :type trained_image: int
    :param unique_id: The `unique_id` parameter in the `insert_classification_model_card` function is a
    string that represents a unique identifier associated with the model card being inserted into the
    database. This identifier is used to uniquely identify and reference the specific model card within
    the database
    :type unique_id: str
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = insert(ModelCard).values(
                created_at=local_time(),
                started_task_at=started_task_at,
                finished_task_at=finished_task_at,
                unique_id=unique_id,
                model_name=model_name,
                model_type=model_type,
                trained_image=trained_image,
            )
            await session.execute(query)
            await session.commit()
            logging.info(
                f"[insert_classification_model_card] Inserted new {model_type} model card."
            )
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[insert_classification_model_card] Error inserting data: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            await session.close()


async def extract_models_card_entry(
    model_type: Literal["classification", "query"],
) -> Row | None:
    """
    The above functions handle extracting and updating model card entries in a database asynchronously.

    :param model_type: The `model_type` parameter in both functions represents the type of model for
    which you want to extract or update the model card entry. It can have one of two literal values:
    "classification" or "query". This parameter is used to filter the model card entries based on their
    model type in the
    :type model_type: Literal["classification", "query"]
    :return: The `extract_models_card_entry` function returns a `Row` object if a model entry is found
    based on the provided `model_type`. If no entry is found, it returns `None`.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(ModelCard).where(ModelCard.model_type == model_type)
            result = await session.execute(query)
            entry = result.fetchone()
            if not entry:
                raise DataNotFoundError(f"Model entry {model_type} not found!")
            return entry
        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[insert_classification_model_card] Error inserting data: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            await session.close()
    return None


async def update_model_card_entry(
    started_task_at: datetime,
    finished_task_at: datetime,
    model_type: Literal["classification", "query"],
    trained_image: int,
) -> None:
    """
    This async function updates a model card entry in a database with specified parameters.

    :param started_task_at: The `started_task_at` parameter represents the datetime when the task
    associated with the model card entry started
    :type started_task_at: datetime
    :param finished_task_at: `finished_task_at` is a parameter representing the datetime when a task
    associated with a model card entry was completed or finished
    :type finished_task_at: datetime
    :param model_type: The `model_type` parameter in the `update_model_card_entry` function represents
    the type of model for which you are updating the model card entry. It can have a value of either
    "classification" or "query", as specified by the `Literal` type annotation in the function
    signature. This parameter
    :type model_type: Literal["classification", "query"]
    :param trained_image: The `trained_image` parameter in the `update_model_card_entry` function
    represents the number of images that were used to train the model specified by the `model_type`.
    This parameter is an integer value that indicates the quantity of images used in the training
    process for the specific model type, which can be
    :type trained_image: int
    """
    async with database_connection(connection_type="async").connect() as session:
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
            await session.execute(query)
            await session.commit()
            logging.info(f"[update_model_card_entry] Updated {model_type} model card.")
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(f"[update_model_card_entry] Error inserting data: {e}")
            await session.rollback()
            raise DatabaseQueryError(detail="Database query failed.")
        finally:
            await session.close()
