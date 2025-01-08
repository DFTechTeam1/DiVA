import httpx
import pytest
from random import randint
from utils.query.image_tag import extract_image_tag_entries


@pytest.mark.asyncio
async def test_labels_description_skipping_parameters() -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate")
        response = res.json()

        assert res.status_code == 200
        assert response["data"] is not None
        assert len(response["data"]["images"]) == 10


@pytest.mark.asyncio
async def test_labels_description_with_valid_page_parameters() -> None:
    params = {"page": 1}
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate", params=params)
        response = res.json()

        assert res.status_code == 200
        assert len(response["data"]["images"]) == 10


@pytest.mark.asyncio
async def test_labels_description_with_valid_image_per_page_parameters() -> None:
    image_per_page = 20
    params = {"image_per_page": image_per_page}

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate", params=params)
        response = res.json()

        assert res.status_code == 200
        assert len(response["data"]["images"]) == image_per_page


@pytest.mark.asyncio
async def test_labels_description_with_valid_is_validated_parameters() -> None:
    params = {"is_validated": True}
    total_validated_images = extract_image_tag_entries(is_validated=True)
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate", params=params)
        response = res.json()

        assert res.status_code == 200
        assert response["data"]["images"] is None if not total_validated_images else total_validated_images


@pytest.mark.asyncio
async def test_labels_description_with_invalid_page_parameters() -> None:
    page = randint(10000, 20000)
    params = {"page": page}
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate", params=params)
        response = res.json()

        assert res.status_code == 200
        assert response["data"]["images"] is None


@pytest.mark.asyncio
async def test_labels_description_with_all_invalid_parameters() -> None:
    page = randint(10000, 20000)
    image_per_page = randint(10000, 20000)
    params = {"page": page, "image_per_page": image_per_page}
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate", params=params)
        response = res.json()

        assert res.status_code == 200
        assert response["data"]["available_page"] == 1
        assert response["data"]["images"] is None
