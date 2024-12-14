from services.postgres.connection import database_connection
from services.postgres.models import ImageTag
from sqlalchemy import select, func
from sqlalchemy.sql import and_
from utils.logger import logging
from utils.custom_errors import DataNotFoundError, DatabaseQueryError


async def extract_distributed_entries(
    page: int, image_per_page: int, ip_address: str, is_validated: bool
) -> list | None:
    async with database_connection(connection_type="async").connect() as session:
        try:
            skip_entry = [
                0 if page == 1 else ((image_per_page * page) - image_per_page)
            ]

            query = (
                select(ImageTag)
                .where(
                    and_(
                        ImageTag.ip_address == ip_address,
                        ImageTag.is_validated == is_validated,
                    )
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
            total_page = total_count // image_per_page if total_count > 1 else 1

            result = await session.execute(query)
            rows = result.fetchall()
            result = [dict(row._mapping) for row in rows]

            if not result:
                result = None

            data = {}
            data["pagination"] = total_page
            data["image_per_page"] = result
            return data
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
