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


@pytest.mark.asyncio
async def test_find_image_with_valid_directory_and_available_images() -> None:
    """Should return list of absolute image paths in directory."""
    image_paths = find_image_path()
    total_image_files = [
        file
        for root, dirs, files in os.walk("/project_utils/diva/client_preview")
        for file in files
        if file.lower().endswith(("jpeg", "jpg", "png"))
    ]
    assert type(image_paths) is list
    assert len(image_paths) == len(total_image_files)


@pytest.mark.asyncio
async def test_find_image_with_mixed_file_and_valid_directory() -> None:
    """Should only return list of image files, excluding other files."""
    image_paths = find_image_path(image_path="images")
    total_image_files = [
        file
        for root, dirs, files in os.walk("images")
        for file in files
        if file.lower().endswith(("jpeg", "jpg", "png"))
    ]
    assert type(image_paths) is list
    assert len(image_paths) == len(total_image_files)
