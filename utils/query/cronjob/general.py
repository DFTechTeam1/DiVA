import csv
import os
from utils.logger import logging
from pathlib import Path


async def save_data(data: list, filename: str) -> None:
    default_path = Path("/project_utils/diva/backup_db")
    default_path.mkdir(parents=True, exist_ok=True)

    filepath = os.path.join(default_path, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    logging.info(f"Data successfully saved to {filepath}")
