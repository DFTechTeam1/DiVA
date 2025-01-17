import pytest
import httpx
from uuid import uuid4
from src.secret import Config

config = Config()


@pytest.mark.asyncio
async def test_create_nas_single_dir_with_valid_payload_using_string() -> None:
    """Should create new single directory"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": "/nas_testing",
        "target_folder": f"api_testing/{str(uuid4())}",
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["non_existing_folder"]) == 1


@pytest.mark.asyncio
async def test_create_nas_single_dir_with_valid_payload_using_array() -> None:
    """Should create new single directory"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": ["/nas_testing"],
        "target_folder": [f"api_testing/{str(uuid4())}"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["non_existing_folder"]) == 1


@pytest.mark.asyncio
async def test_create_nas_multi_dir_with_valid_payload() -> None:
    """Should create new multi directory"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": ["/nas_testing", "/nas_testing", "/nas_testing"],
        "target_folder": [
            f"api_testing/{str(uuid4())}",
            f"api_testing/{str(uuid4())}",
            f"api_testing/{str(uuid4())}",
        ],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["non_existing_folder"]) == len(
            payload["target_folder"]
        )


@pytest.mark.asyncio
async def test_create_nas_single_directory_already_exist_in_nas():
    """Should skip creating directory due to target_folder already exist on NAS"""

    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": "/nas_testing",
        "target_folder": "existing_dir/already_exist1",
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["folder_already_exsist"]) == 1


@pytest.mark.asyncio
async def test_create_nas_multi_directory_all_already_exist_in_nas():
    """Should skip creating dir due to all dir already exist on NAS"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": ["/nas_testing", "/nas_testing", "/nas_testing"],
        "target_folder": [
            "existing_dir/already_exist1",
            "existing_dir/already_exist2",
            "existing_dir/already_exist3",
        ],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["folder_already_exsist"]) == len(
            payload["target_folder"]
        )
        assert response["data"]["non_existing_folder"] is None


@pytest.mark.asyncio
async def test_create_nas_multi_directory_mix_of_new_and_dir_already_exist_on_nas():
    """Should skip creating existing dir on NAS and only create non-existing dir"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": ["/nas_testing", "/nas_testing", "/nas_testing"],
        "target_folder": [
            f"api_testing/{str(uuid4())}",
            "existing_dir/already_exist1",
            "existing_dir/already_exist2",
        ],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert len(response["data"]["folder_already_exsist"]) == 2
        assert len(response["data"]["non_existing_folder"]) == 1


@pytest.mark.asyncio
async def test_create_nas_with_invalid_shared_folder_params_using_array():
    """Should raise Bad Request error due to invalid shared folder payload"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": ["nas_testing"],
        "target_folder": [f"api_testing/{str(uuid4())}"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_nas_with_invalid_shared_folder_params_using_string():
    """Should raise Bad Request error due to invalid shared folder payload"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": "nas_testing",
        "target_folder": f"api_testing/{str(uuid4())}",
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_nas_with_invalid_shared_folder_and_target_folder_params():
    """Should raise Bad Request error due to shared folder and target folder should in same data type"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "shared_folder": "nas_testing",
        "target_folder": [f"api_testing/{str(uuid4())}"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/create-dir", json=payload)
        assert res.status_code == 400
