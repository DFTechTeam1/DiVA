import os
import string
import random
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from utils.logger import logging
from utils.custom_errors import DataNotFoundError


def find_image_path(
    image_path: str = "/home/dfactory/custom_nas",
) -> list | None:
    """
    The function `find_image_path` takes an image path as input, checks if the directory exists, finds
    image files with specific extensions in the directory, and returns a list of image paths.

    :param image_path: The `image_path` parameter in the `find_image_path` function is a string that
    represents the directory path where the images are located. By default, it is set to
    "/project_utils/diva/client_preview". This function is designed to find all image files (with
    extensions .jpg, .jpeg, defaults to /project_utils/diva/client_preview
    :type image_path: str (optional)
    :return: A list of image file paths is being returned by the `find_image_path` function.
    """
    default_path = Path(image_path)

    try:
        if not os.path.exists(path=default_path):
            raise DataNotFoundError(detail="Directory not found!")

        image_extensions = {".jpg", ".jpeg", ".png"}

        image_paths = [str(path) for path in Path(default_path).rglob("*") if path.suffix.lower() in image_extensions]

        if not image_paths:
            logging.error(f"[find_image_path] No image files found in {default_path}")
            raise DataNotFoundError(detail="No image found!")

        return image_paths

    except DataNotFoundError:
        raise
    except Exception as e:
        logging.error(f"[find_image_path] Exception error raised: {e}")

    return None


def extract_filename(filepaths: list) -> list:
    """
    The function `extract_filename` takes a list of filepaths and returns a list of filenames by
    extracting the last part of each filepath after the last '/' character.

    :param filepaths: A list of file paths that you want to extract the filenames from
    :type filepaths: list
    :return: The function `extract_filename` takes a list of filepaths as input and returns a list of
    filenames extracted from the filepaths by splitting them at the "/" character and taking the last
    element.
    """
    return [filename.split("/")[-1] for filename in filepaths]


def local_time() -> datetime:
    return datetime.now()


def generate_random_word(length: int = 4) -> str:
    """
    The function `generate_random_word` creates a random word of a specified length using lowercase
    letters.

    :param length: The `length` parameter in the `generate_random_word` function specifies the length of
    the random word that will be generated. By default, if no length is provided, the function will
    generate a random word of length 4. You can also specify a custom length if you want a word of a,
    defaults to 4
    :type length: int (optional)
    :return: A random word consisting of lowercase letters with the specified length is being returned.
    """
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
