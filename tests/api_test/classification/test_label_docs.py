import pytest
import httpx

@pytest.mark.asyncio
async def test_labels_description_with_valid_request() -> None:
    expected_categories = ["object", "environment", "design_type", "time_period", "dominant_colors", "culture_styles"]

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.get("/api/v1/classification/label-docs")
        response = res.json()

        assert res.status_code == 200
        assert response["data"] is not None
        assert type(response["data"]["documentation"]) is list

        categories = [doc["category"] for doc in response["data"]["documentation"]]

        for category in expected_categories:
            assert category in categories
