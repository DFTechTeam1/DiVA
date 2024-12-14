from sqlalchemy import update
from services.postgres.connection import database_connection
from services.postgres.models import ImageTag
from utils.custom_errors import DatabaseQueryError, DataNotFoundError
from utils.logger import logging


async def update_labels(
    image_id: int,
    artifacts: bool = False,
    nature: bool = False,
    living_beings: bool = False,
    natural: bool = False,
    manmade: bool = False,
    conceptual: bool = False,
    art_deco: bool = False,
    architectural: bool = False,
    artistic: bool = False,
    sci_fi: bool = False,
    fantasy: bool = False,
    day: bool = False,
    afternoon: bool = False,
    evening: bool = False,
    night: bool = False,
    warm: bool = False,
    cool: bool = False,
    neutral: bool = False,
    gold: bool = False,
    asian: bool = False,
    european: bool = False,
) -> dict | None:
    async with database_connection(connection_type="async").connect() as session:
        try:
            update_values = {
                "artifacts": artifacts,
                "nature": nature,
                "living_beings": living_beings,
                "natural": natural,
                "manmade": manmade,
                "conceptual": conceptual,
                "art_deco": art_deco,
                "architectural": architectural,
                "artistic": artistic,
                "sci_fi": sci_fi,
                "fantasy": fantasy,
                "day": day,
                "afternoon": afternoon,
                "evening": evening,
                "night": night,
                "warm": warm,
                "cool": cool,
                "neutral": neutral,
                "gold": gold,
                "asian": asian,
                "european": european,
                "is_validated": True,
            }

            # Construct the update query
            query = (
                update(ImageTag)
                .where(ImageTag.id == image_id)
                .values(update_values)
                .returning(
                    *ImageTag.__table__.columns
                )  # Return all columns after update
            )

            # Execute the query
            result = await session.execute(query)
            await session.commit()  # Commit the transaction

            # Fetch the updated row
            row = result.fetchone()

            if not row:
                logging.error(
                    f"[update_labels] No entry found for ImageTag with ID: {image_id}"
                )
                raise DataNotFoundError(detail="Data entry not found")

        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(f"[update_labels] Error while updating labels: {e}")
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()
    return None
