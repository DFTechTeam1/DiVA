import sys
import csv
import os
import asyncio
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from services.postgres.models import ImageTag
from utils.query.labels_documentation import retrieve_all


async def save_data(data: list) -> None:
    default_path = Path("/project-utils/backup")
    default_path.mkdir(parents=True, exist_ok=True)

    filename = "backup_image_tag.csv"
    filepath = os.path.join(default_path, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    logging.info(f"Data successfully saved to {filepath}")


async def main():
    data = await retrieve_all(table_model=ImageTag)
    await save_data(data=data)


asyncio.run(main())
