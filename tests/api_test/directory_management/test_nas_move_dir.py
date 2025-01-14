import pytest
import httpx
from src.secret import Config
from random import randint
from utils.nas.external import list_folder


config = Config()
destination = "/nas_testing/move_dir_target"


@pytest.mark.asyncio
async def test_move_nas_single_dir_with_valid_payload_using_string() -> None:
    """Should remove a single directory"""
    existing_dir = await list_folder(ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing")
    random_index = randint(0, len(existing_dir) - 1)
    random_path = existing_dir[random_index]["path"]

    payload = {"ip_address": config.NAS_IP_5, "target_folder": random_path, "dest_folder_path": destination}

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/move-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory successfully moved."
        assert response["data"]["folder_already_exsist"] is None
        assert response["data"]["non_existing_folder"] is None


@pytest.mark.asyncio
async def test_move_nas_multi_dir_with_valid_payload_using_array() -> None:
    """Should remove a multi directory"""
    existing_dir = await list_folder(ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing")
    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            existing_dir[randint(0, len(existing_dir) - 1)]["path"],
            existing_dir[randint(0, len(existing_dir) - 1)]["path"],
        ],
        "dest_folder_path": [destination, destination],
    }

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/move-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory successfully moved."
        assert response["data"]["folder_already_exsist"] is None
        assert response["data"]["non_existing_folder"] is None
