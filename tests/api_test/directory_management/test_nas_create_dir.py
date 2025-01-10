import pytest
import httpx
from faker import Faker
from src.schema.request_format import NasDirectoryManagement

faker = Faker()


@pytest.mark.asyncio
async def test_create_nas_single_dir_with_valid_payload_using_string() -> None:
    payload = NasDirectoryManagement(
        ip_address="192.168.100.105", folder_path="/apitesting", directory_name=f"bas/{faker.prefix_male()}"
    )
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload.model_dump())
        assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_nas_single_dir_with_valid_payload_using_array() -> None:
    payload = NasDirectoryManagement(
        ip_address="192.168.100.105", folder_path="/apitesting", directory_name=["bas/aaa", "bas/aaa", "bas/aaa"]
    )
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload.model_dump())
        assert res.status_code == 200
