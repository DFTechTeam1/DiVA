import pytest
import httpx
from src.secret import Config
from utils.nas.external import list_folder
from faker import Faker

config = Config()
faker = Faker()


@pytest.mark.asyncio
async def test_update_nas_single_dir_with_valid_payload_using_string() -> None:
    """Should update single directory using string data type"""

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": existing_dir[0]["path"],
        "changed_name_into": f"{faker.name()}",
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory renamed successfully."
        assert len(response["data"]["non_existing_folder"]) == 1
        assert response["data"]["folder_already_exist"] is None


@pytest.mark.asyncio
async def test_update_nas_single_dir_with_valid_payload_using_array() -> None:
    """Should update single directory using list data type"""

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )
    random_path = existing_dir[0]["path"]

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [random_path],
        "changed_name_into": [f"{faker.name()}"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory renamed successfully."
        assert len(response["data"]["non_existing_folder"]) == 1
        assert response["data"]["folder_already_exist"] is None


@pytest.mark.asyncio
async def test_update_nas_multi_dir_with_valid_payload_using_array() -> None:
    """
    Should update multi directory from array 0-9 and 10-19 on /nas_testing/api_testing
    and update them using faker.name
    """

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            existing_dir[0]["path"],
            existing_dir[1]["path"],
        ],
        "changed_name_into": [f"{faker.name()}", f"{faker.name()}"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "Directory renamed successfully."
        assert len(response["data"]["non_existing_folder"]) == len(
            payload["changed_name_into"]
        )
        assert response["data"]["folder_already_exist"] is None


@pytest.mark.asyncio
async def test_update_nas_multi_dir_with_mix_directory_using_array() -> None:
    """
    Should update multi directory from array 0-9 and 10-19 on /nas_testing/api_testing
    and update them using faker.name(), but skip the update in the last data
    due to targeting an existing dir
    """

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [
            existing_dir[0]["path"],
            existing_dir[1]["path"],
            existing_dir[2]["path"],
        ],
        "changed_name_into": [
            f"{faker.name()}",
            f"{faker.name()}",
            "4662f3c4-4adc-4736-842d-36b7a55067f3",
        ],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        print(res)
        response = res.json()
        print(response)
        assert res.status_code == 200
        assert response["message"] == "Directory renamed successfully."
        assert len(response["data"]["folder_already_exist"]) == 1
        assert len(response["data"]["non_existing_folder"]) == 2


@pytest.mark.asyncio
async def test_update_nas_single_dir_with_change_name_into_directory_already_exist_using_string() -> (
    None
):
    """Should skipping update directory due to changed_name_into and matched into existing dir on NAS"""

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": existing_dir[0]["path"],
        "changed_name_into": "4662f3c4-4adc-4736-842d-36b7a55067f3",
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        response = res.json()
        assert res.status_code == 200
        assert response["message"] == "All target folder already exist."
        assert response["data"]["non_existing_folder"] is None
        assert len(response["data"]["folder_already_exist"]) == 1


@pytest.mark.asyncio
async def test_update_nas_single_dir_with_invalid_data_type() -> None:
    """Should raise error due to changed_name_into and target_folder should in same data type"""

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": existing_dir[0]["path"],
        "changed_name_into": ["4662f3c4-4adc-4736-842d-36b7a55067f3"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        assert res.status_code == 400


@pytest.mark.asyncio
async def test_update_nas_single_dir_with_invalid_length_of_payload() -> None:
    """Should raise error due to changed_name_into and target_folder should in same length"""

    existing_dir = await list_folder(
        ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
    )

    payload = {
        "ip_address": config.NAS_IP_5,
        "target_folder": [existing_dir[0]["path"]],
        "changed_name_into": ["already_exist_dir1", "already_exist_dir2"],
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        res = await client.post("/api/v1/nas/update-dir", json=payload)
        assert res.status_code == 400
