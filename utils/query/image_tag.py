from utils.logger import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.request_format import AllowedIpAddress
from utils.helper import find_image_path, extract_filename
from utils.custom_errors import DatabaseQueryError
from services.postgres.models import ImageTag
from services.postgres.connection import database_connection
from utils.query.labels_documentation import validate_data_availability


async def insert_image_tag_entry(
    filepaths: list[str],
    filenames: list[str],
    allowed_ips: list = None,
):
    allowed_ips = AllowedIpAddress()
    total_entries = len(filenames)
    total_ips = len(allowed_ips.ip_address)

    if total_entries < total_ips:
        raise ValueError("Data entry cannot less than allowed ip.")

    base_count = total_entries // total_ips
    remainder = total_entries % total_ips

    distributed_data = []
    start_index = 0

    for idx_ips, ip in enumerate(allowed_ips.ip_address):
        end_index = start_index + base_count + (1 if idx_ips < remainder else 0)
        entries = [
            ImageTag(
                filepath=filepaths[idx_file],
                filename=filenames[idx_file],
                ip_address=ip,
            )
            for idx_file in range(start_index, end_index)
        ]
        distributed_data.extend(entries)
        start_index = end_index

    async_engine = database_connection(connection_type="async")
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            session.add_all(distributed_data)
            await session.commit()
            logging.info("Insert image_tag entries.")
        except Exception as e:
            logging.error(f"[insert_image_tag_entry] Error inserting data: {e}")
            await session.rollback()
            raise DatabaseQueryError(detail="Database query failed")
        finally:
            await session.close()


async def initialize_image_tag_preparation():
    is_available = await validate_data_availability(table_model=ImageTag)
    if not is_available:
        filepaths = find_image_path()
        filenames = extract_filename(filepaths=filepaths)
        await insert_image_tag_entry(filepaths=filepaths, filenames=filenames)
