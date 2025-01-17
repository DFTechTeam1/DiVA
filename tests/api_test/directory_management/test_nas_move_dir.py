# import pytest
# import httpx
# from uuid import uuid4
# from src.secret import Config
# from random import randint
# from utils.nas.external import list_folder


# config = Config()
# destination = "/nas_testing/move_dir_target"


# @pytest.mark.asyncio
# async def test_move_nas_single_dir_with_valid_payload_using_string() -> None:
#     """Should remove a single directory"""
#     existing_dir = await list_folder(
#         ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
#     )
#     random_index = randint(0, len(existing_dir) - 1)
#     random_path = existing_dir[random_index]["path"]

#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": random_path,
#         "dest_folder_path": destination,
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         response = res.json()
#         assert res.status_code == 200
#         assert response["message"] == "Directory successfully moved."
#         assert len(response["data"]["folder_already_exsist"]) == 1
#         assert response["data"]["non_existing_folder"] is None


# @pytest.mark.asyncio
# async def test_move_nas_multi_dir_with_valid_payload_using_array() -> None:
#     """Should remove a multi directory"""
#     existing_dir = await list_folder(
#         ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
#     )
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": [
#             existing_dir[randint(0, len(existing_dir) - 1)]["path"],
#             existing_dir[randint(0, len(existing_dir) - 1)]["path"],
#         ],
#         "dest_folder_path": [destination, destination],
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         print(res)
#         response = res.json()
#         print(response)
#         assert res.status_code == 200
#         assert response["message"] == "Directory successfully moved."
#         assert len(response["data"]["folder_already_exsist"]) == len(
#             payload["target_folder"]
#         )
#         assert response["data"]["non_existing_folder"] is None


# @pytest.mark.asyncio
# async def test_move_nas_multi_dir_with_mix_existing_and_non_existing_nas_dir() -> None:
#     """Should move only existing dir on nas"""
#     existing_dir = await list_folder(
#         ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
#     )
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": [
#             existing_dir[
#                 randint(
#                     0,
#                     len(
#                         await list_folder(
#                             ip_address=config.NAS_IP_5,
#                             directory_path="/nas_testing/api_testing",
#                         )
#                     )
#                     - 1,
#                 )
#             ]["path"],
#             existing_dir[
#                 randint(
#                     0,
#                     len(
#                         await list_folder(
#                             ip_address=config.NAS_IP_5,
#                             directory_path="/nas_testing/api_testing",
#                         )
#                     )
#                     - 1,
#                 )
#             ]["path"],
#             f"/nas_testing/api_testing/{str(uuid4())}",
#         ],
#         "dest_folder_path": [destination, destination, destination],
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         response = res.json()
#         assert res.status_code == 200
#         assert response["message"] == "Directory successfully moved."
#         assert len(response["data"]["folder_already_exsist"]) == 2
#         assert response["data"]["non_existing_folder"] is None


# @pytest.mark.asyncio
# async def test_move_nas_non_existing_directory_on_nas() -> None:
#     """Should not move NAS directory due to non existing directory"""
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": f"/nas_testing/api_testing/{str(uuid4())}",
#         "dest_folder_path": destination,
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         response = res.json()
#         assert res.status_code == 200
#         assert (
#             response["message"] == "Target folder should be existing directory on NAS."
#         )
#         assert response["data"]["folder_already_exsist"] is None
#         assert len(response["data"]["non_existing_folder"]) == 1


# @pytest.mark.asyncio
# async def test_move_nas_non_with_invalid_target_folder_params() -> None:
#     """Should raise error due to invalid target folder params"""
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": "random_folder/random_sub_folder",
#         "dest_folder_path": destination,
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         assert res.status_code == 400


# @pytest.mark.asyncio
# async def test_move_nas_non_with_invalid_destination_folder_path_params() -> None:
#     """Should raise error due to non existing destination folder path param"""
#     existing_dir = await list_folder(
#         ip_address=config.NAS_IP_5, directory_path="/nas_testing/api_testing"
#     )
#     random_index = randint(0, len(existing_dir) - 1)
#     random_path = existing_dir[random_index]["path"]
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": random_path,
#         "dest_folder_path": "/nas_testing/random_destination_dir",
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         response = res.json()
#         assert res.status_code == 200
#         assert (
#             response["message"]
#             == "Destination folder should be existing directory on NAS."
#         )
#         assert response["data"]["folder_already_exsist"] is None
#         assert len(response["data"]["non_existing_folder"]) == 1


# @pytest.mark.asyncio
# async def test_move_nas_non_with_invalid_length_of_target_folder_and_destination_path() -> (
#     None
# ):
#     """Should raise error due to length of target folder and destination folder path should be equal"""
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": [
#             "/nas_testing/api_testing/tetsing1",
#             "/nas_testing/api_testing/tetsing1",
#         ],
#         "dest_folder_path": [destination],
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         assert res.status_code == 400


# @pytest.mark.asyncio
# async def test_move_nas_with_duplicated_target_folder() -> None:
#     """Should raise error due to target folder value should be unique"""
#     payload = {
#         "ip_address": config.NAS_IP_5,
#         "target_folder": [
#             "/nas_testing/api_testing/tetsing1",
#             "/nas_testing/api_testing/tetsing1",
#         ],
#         "dest_folder_path": [destination, destination],
#     }

#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         res = await client.post("/api/v1/nas/move-dir", json=payload)
#         assert res.status_code == 400
