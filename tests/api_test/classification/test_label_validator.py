import pytest
import httpx
from random import randint


@pytest.mark.asyncio
async def test_validate_label_with_valid_image_id() -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/paginate")
        response = res.json()
        image_id = response["data"]["images"][0]["id"]

        assert res.status_code == 200
        assert response["data"] is not None
        assert len(response["data"]["images"]) == 10

        params = {"image_id": image_id}
        payload = {
            "artifacts": False,
            "nature": False,
            "living_beings": False,
            "natural": False,
            "manmade": False,
            "conceptual": False,
            "art_deco": False,
            "heaven": False,
            "architectural": False,
            "artistic": False,
            "sci_fi": False,
            "fantasy": False,
            "day": False,
            "afternoon": False,
            "evening": False,
            "night": False,
            "warm": False,
            "cool": False,
            "neutral": False,
            "gold": False,
            "asian": False,
            "european": False,
        }

        res = await client.patch(
            f"/api/v1/classification/validator/{image_id}", params=params, json=payload
        )
        assert res.status_code == 200


@pytest.mark.asyncio
async def test_validate_label_with_invalid_image_id() -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        image_id = randint(100000, 999999)
        params = {"image_id": image_id}
        payload = {
            "artifacts": False,
            "nature": False,
            "living_beings": False,
            "natural": False,
            "manmade": False,
            "conceptual": False,
            "art_deco": False,
            "heaven": False,
            "architectural": False,
            "artistic": False,
            "sci_fi": False,
            "fantasy": False,
            "day": False,
            "afternoon": False,
            "evening": False,
            "night": False,
            "warm": False,
            "cool": False,
            "neutral": False,
            "gold": False,
            "asian": False,
            "european": False,
        }

        res = await client.patch(
            f"/api/v1/classification/validator/{image_id}", params=params, json=payload
        )
        assert res.status_code == 404
