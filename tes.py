import os
from pathlib import Path
from utils.logger import logging
from utils.custom_errors import DataNotFoundError


def find_image_path() -> list:
    default_path = Path("/home/dfactory/client_preview")
    if not os.path.exists(path=default_path):
        raise DataNotFoundError(
            detail="Directory not found! Please make sure you already mount directory."
        )

    image_extensions = {".jpg", ".jpeg", ".png"}
    image_paths = [
        str(path)
        for path in Path(default_path).rglob("*")
        if path.suffix.lower() in image_extensions
    ]

    if not image_paths:
        logging.error(f"[find_image_path] No image files found in {default_path}")
        raise DataNotFoundError(detail="No image found!")

    return image_paths


print(len(find_image_path()))
