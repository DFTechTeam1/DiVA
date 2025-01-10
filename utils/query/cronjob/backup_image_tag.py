import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from utils.helper import save_data
from services.postgres.connection import get_db
from services.postgres.models import ImageTag
from utils.query.general import find_record
from utils.logger import logging


async def backup_image_tag():
    async for db in get_db():
        data = await find_record(db=db, table=ImageTag, fetch_type="all")
        break
    if data:
        await save_data(data=data, filename="backup_image_tag.csv")
    else:
        logging.warning("Image tag data is empty.")


asyncio.run(backup_image_tag())
