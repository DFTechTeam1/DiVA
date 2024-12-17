import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from utils.query.cronjob.backup import save_data
from services.postgres.models import ImageTag
from utils.query.labels_documentation import retrieve_all


async def backup_image_tag():
    data = await retrieve_all(table_model=ImageTag)
    await save_data(data=data, filename="backup_image_tag.csv")


asyncio.run(backup_image_tag())
