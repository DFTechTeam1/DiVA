from utils.logger import logging
from services.postgres.connection import database_connection
from services.postgres.models import ImageTag
from sqlalchemy import select, func
from sqlalchemy.sql import and_
from utils.custom_error import DataNotFoundError, DatabaseQueryError
from src.schema.response import Pagination


async def extract_distributed_entries(
    page: int, image_per_page: int, ip_address: str, is_validated: bool
) -> Pagination:
    response = Pagination()

    async with database_connection(connection_type="async").connect() as session:
        try:
            skip_entry = [
                0 if page == 1 else ((image_per_page * page) - image_per_page)
            ]

            query = (
                select(ImageTag)
                .where(
                    ImageTag.ip_address == ip_address,
                    ImageTag.is_validated == is_validated,
                )
                .limit(image_per_page)
                .offset(skip_entry[0])
                .order_by(ImageTag.id)
            )

            total_count_query = (
                select(func.count())
                .where(
                    and_(
                        ImageTag.ip_address == ip_address,
                        ImageTag.is_validated == is_validated,
                    )
                )
                .select_from(ImageTag)
            )
            result = await session.execute(total_count_query)
            total_count = result.scalar_one_or_none()

            total_page = (total_count + image_per_page - 1) // image_per_page

            result = await session.execute(query)
            rows = result.fetchall()
            result = [dict(row._mapping) for row in rows]

            response.available_page = total_page
            response.images = result

            return response

        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[extract_distributed_entries] Error while extracting pagination: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query.")
        finally:
            await session.close()

    return None
