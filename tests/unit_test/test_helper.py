import os
import pytest
import random

from pathlib import Path
from utils.helper import generate_random_word
from utils.custom_errors import DataNotFoundError
from utils.helper import find_image_path


@pytest.mark.asyncio
async def test_find_image_paths_with_invalid_directory() -> None:
    """Should raise error due invalid directory."""
    random_path = Path(f"{generate_random_word()}/{generate_random_word()}")
    with pytest.raises(DataNotFoundError, match="Directory not found!"):
        await find_image_path(image_path=random_path)


@pytest.mark.asyncio
async def test_find_image_paths_with_valid_directory_but_no_images_data() -> None:
    """Should raise error due to no images found in the directory."""
    project_dir = os.getcwd()
    services_dir = Path("services")
    full_path = os.path.join(project_dir, services_dir)
    list_path = os.listdir(full_path)
    random_path = list_path[random.randint(0, (len(list_path) - 1))]
    fixed_path = os.path.join(full_path, random_path)
    with pytest.raises(DataNotFoundError, match="No image found!"):
        await find_image_path(image_path=fixed_path)
