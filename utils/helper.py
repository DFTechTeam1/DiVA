import os
import string
import csv
import random
from src.secret import Config
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from utils.logger import logging
from utils.custom_error import DataNotFoundError


async def save_data(data: list, filename: str) -> None:
    home_path = Path.home()
    default_path = Path(f"{home_path}/Project/utils/diva/backup_db")
    default_path.mkdir(parents=True, exist_ok=True)

    filepath = os.path.join(default_path, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    logging.info(f"Data successfully saved to {filepath}")


def find_image_path(image_path: str = None) -> list[str]:
    try:
        # Use provided path or fall back to default
        home_path = Path.home()
        default_path = Path(f"{home_path}/Project/utils/diva/client_preview")
        target_path = Path(image_path) if image_path else default_path

        # Check if the directory exists
        if not target_path.exists():
            raise DataNotFoundError(detail="Directory not found!")

        # Search for image files
        image_extensions = {".jpg", ".jpeg", ".png"}
        image_paths = [str(path) for path in target_path.rglob("*") if path.suffix.lower() in image_extensions]

        if not image_paths:
            raise DataNotFoundError(detail="No image found!")

        return image_paths

    except DataNotFoundError as e:
        logging.error(f"[find_image_path] {e.detail}")
        raise

    except Exception as e:
        logging.error(f"[find_image_path] Unexpected exception: {e}")
        raise


def extract_filename(filepaths: list) -> list:
    return [filename.split("/")[-1] for filename in filepaths]


def local_time() -> datetime:
    return datetime.now()


def port_matcher(ip_address: str) -> str:
    config = Config()
    if ip_address == "192.168.100.101":
        return config.NAS_PORT_2
    return config.NAS_PORT_1


def generate_random_word(length: int = 4) -> str:
    if length < 1:
        raise ValueError("length parameter should be more than 0")

    alphabet = string.ascii_lowercase
    word = "".join(random.choice(alphabet) for _ in range(length))

    return word


def label_distribution(entries: list) -> None:
    label_counts = defaultdict(lambda: {"true": 0, "false": 0})

    for entry in entries:
        for label, value in entry.items():
            if isinstance(value, bool) and label not in {"is_validated"}:
                if value:
                    label_counts[label]["true"] += 1
                else:
                    label_counts[label]["false"] += 1

    total_entries = len(entries)
    label_percentages = {
        label: {
            "true": (counts["true"] / total_entries) * 100,
            "false": (counts["false"] / total_entries) * 100,
        }
        for label, counts in label_counts.items()
    }

    for label, percentages in label_percentages.items():
        logging.info(f"{label}: True = {percentages['true']:.2f}%, False = {percentages['false']:.2f}%")
