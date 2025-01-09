import pytest
from pathlib import Path
from utils.helper import find_image_path
from utils.custom_error import DataNotFoundError


@pytest.mark.asyncio
async def test_find_image_paths_with_valid_directory_and_available_data():
    """Test with a directory containing only image files."""
    test_dir = Path("./test_images_dir")
    test_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "image1.jpg").touch()
        (test_dir / "image2.png").touch()

        image_paths = find_image_path(image_path=str(test_dir))
        assert len(image_paths) == 2
        assert all(path.endswith(("jpg", "png")) for path in image_paths)
    finally:
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_mixed_files():
    """Test with a directory containing mixed file types."""
    test_dir = Path("./mixed_test_dir")
    test_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "image1.jpg").touch()
        (test_dir / "image2.png").touch()
        (test_dir / "document.txt").touch()
        (test_dir / "script.py").touch()

        image_paths = find_image_path(image_path=str(test_dir))
        assert len(image_paths) == 2
        assert all(path.endswith(("jpg", "png")) for path in image_paths)
    finally:
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_subdirectories():
    """Test with a directory containing subdirectories."""
    test_dir = Path("./test_dir_with_subdirs")
    sub_dir = test_dir / "subdir"
    test_dir.mkdir(parents=True, exist_ok=True)
    sub_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "image1.jpg").touch()
        (sub_dir / "image2.png").touch()

        image_paths = find_image_path(image_path=str(test_dir))
        assert len(image_paths) == 2
    finally:
        for sub in sub_dir.iterdir():
            sub.unlink()
        sub_dir.rmdir()
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_different_image_extensions():
    """Test with a variety of image file extensions."""
    test_dir = Path("./test_images_variety")
    test_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "image1.jpeg").touch()
        (test_dir / "image2.bmp").touch()
        (test_dir / "image3.gif").touch()

        image_paths = find_image_path(image_path=str(test_dir))
        assert len(image_paths) == 1
        assert all(path.endswith(("jpeg")) for path in image_paths)
    finally:
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_special_characters_in_names():
    """Test with files that have special characters in their names."""
    test_dir = Path("./test_special_characters")
    test_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "im@ge1.jpg").touch()
        (test_dir / "image#2.png").touch()

        image_paths = find_image_path(image_path=str(test_dir))
        assert len(image_paths) == 2
        assert any(path.endswith("im@ge1.jpg") for path in image_paths)
        assert any(path.endswith("image#2.png") for path in image_paths)
    finally:
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_non_image_extensions():
    """Test with files having image-like names but non-image extensions."""
    test_dir = Path("./test_non_image_extensions")
    test_dir.mkdir(parents=True, exist_ok=True)
    try:
        (test_dir / "image1.txt").touch()
        (test_dir / "image2.py").touch()

        with pytest.raises(DataNotFoundError, match="No image found!"):
            find_image_path(image_path=str(test_dir))
    finally:
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()


@pytest.mark.asyncio
async def test_find_image_paths_with_invalid_directory():
    """Test with a non-existent directory."""
    invalid_path = Path("/invalid_directory")
    with pytest.raises(DataNotFoundError, match="Directory not found!"):
        find_image_path(image_path=str(invalid_path))


@pytest.mark.asyncio
async def test_find_image_paths_with_valid_directory_and_empty_data():
    """Test with a valid directory but no files."""
    empty_dir = Path("./empty_test_dir")
    empty_dir.mkdir(parents=True, exist_ok=True)
    try:
        with pytest.raises(DataNotFoundError, match="No image found!"):
            find_image_path(image_path=str(empty_dir))
    finally:
        empty_dir.rmdir()
