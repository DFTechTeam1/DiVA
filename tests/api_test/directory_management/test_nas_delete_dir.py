import pytest
import httpx
from src.secret import Config
from random import randint
from utils.nas.external import list_folder
from uuid import uuid4


config = Config()


@pytest.mark.asyncio
async def test_delete_nas_single_dir_with_valid_payload_using_string() -> None:
    """Should remove a single directory"""
    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )
    random_index = randint(0, len(existing_dir) - 1)
    random_path = existing_dir[random_index]["path"]

    payload = {"ip_address": config.NAS_IP_5, "target_folder": random_path}

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory successfully removed."
        assert len(response["data"]["folder_already_exsist"]) == 1
        assert response["data"]["non_existing_folder"] is None


@pytest.mark.asyncio
async def test_delete_nas_multi_dir_with_valid_payload_using_array() -> None:
    """Should remove a multi directory"""
    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )
    random_index = randint(0, len(existing_dir) - 1)

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            existing_dir[random_index]["path"],
            existing_dir[random_index]["path"],
            existing_dir[random_index]["path"],
        ],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory successfully removed."
        assert len(response["data"]["folder_already_exsist"]) == len(
            payload["target_folder"]
        )
        assert response["data"]["non_existing_folder"] is None


@pytest.mark.asyncio
async def test_delete_nas_multi_dir_with_non_existing_folder_on_nas() -> None:
    """Should skip remove directory due to all directory not-exist"""

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            f"/nas_testing/api_testing/{str(uuid4())}",
            f"/nas_testing/api_testing/{str(uuid4())}",
            f"/nas_testing/api_testing/{str(uuid4())}",
        ],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Input should be existing directory on NAS."
        assert len(response["data"]["non_existing_folder"]) == len(
            payload["target_folder"]
        )
        assert response["data"]["folder_already_exsist"] is None


@pytest.mark.asyncio
async def test_delete_nas_multi_dir_with_directory_already_exist_and_new_directory_input() -> (
    None
):
    """Should remove a multi directory"""
    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )
    random_index = randint(0, len(existing_dir) - 1)

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            existing_dir[random_index]["path"],
            existing_dir[random_index]["path"],
            f"/nas_testing/api_testing/{str(uuid4())}",
        ],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory successfully removed."
        assert len(response["data"]["non_existing_folder"]) == 1
        assert len(response["data"]["folder_already_exsist"]) == 2


@pytest.mark.asyncio
async def test_delete_nas_single_dir_with_invalid_shared_folder_params_using_array() -> (
    None
):
    """Should skip deletion directory due to folder not found"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": ["random_shared_folder/also_random_dir"],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Input should be existing directory on NAS."
        assert response["data"]["folder_already_exsist"] is None
        assert len(response["data"]["non_existing_folder"]) == 1


@pytest.mark.asyncio
async def test_delete_nas_single_dir_with_invalid_shared_folder_params_using_string() -> (
    None
):
    """Should skip deletion directory due to folder not found"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": "random_shared_folder/also_random_dir",
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Input should be existing directory on NAS."
        assert len(response["data"]["non_existing_folder"]) == 1
        assert response["data"]["folder_already_exsist"] is None


@pytest.mark.asyncio
async def test_delete_nas_multi_dir_with_invalid_shared_folder_params_using_array() -> (
    None
):
    """Should skip deletion directory due to folder not found"""
    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            "random_shared_folder/also_random_dir1",
            "random_shared_folder/also_random_dir2",
        ],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/delete-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Input should be existing directory on NAS."
        assert response["data"]["folder_already_exsist"] is None
        assert len(response["data"]["non_existing_folder"]) == 2
