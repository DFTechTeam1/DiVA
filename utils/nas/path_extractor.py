import json
import httpx
from typing import Union
from utils.logger import logging
from src.secret import Config
from src.schema.request_format import (
    LoginNasApi,
    LogoutNasApi,
    ListShareNasApi,
    CreateFolderNasApi,
    UpdateFolderNasApi,
    DeleteFolderNasApi,
    MoveFolderNasApi,
)
from utils.custom_error import (
    NasIntegrationError,
    DataNotFoundError,
    ServicesConnectionError,
)


def port_matcher(ip_address: str) -> str:
    config = Config()
    if ip_address == "192.168.100.101":
        return config.NAS_PORT_2
    return config.NAS_PORT_1


def grab_shared_dir(path: str | list[str]) -> str | None:
    logging.debug(f"[grab_shared_dir] Received path: {path}")
    try:
        if isinstance(path, str) and path.startswith("/"):
            logging.info("[grab_shared_dir] Single directory.")
            return "/" + path.split("/")[1]
        if isinstance(path, list) and len(path) != 0 and path[0].startswith("/"):
            logging.info("[grab_shared_dir] Multi directory.")
            return "/" + path[0].split("/")[1]
        if isinstance(path, list) and (not path or not path[0].startswith("/")):
            raise NasIntegrationError(
                detail="folder_path should contain at least 1 value startswith '/' as array of string (e.g: ['/Dfactory/...'])."
            )
        if isinstance(path, str) and not path.startswith("/") or isinstance(path, list) and not path[0].startswith("/"):
            raise NasIntegrationError(detail="folder_path should be startswith '/' (e.g: /Dfactory/...).")
    except NasIntegrationError:
        raise
    except Exception as e:
        logging.error(f"[grab_shared_dir] Error while grab shared path: {e}.")
    return None


def validate_shared_directory(data: dict, folder_path: str) -> bool:
    logging.info("[validate_shared_directory] Searching shared directory.")
    for data in data["data"]["shares"]:
        if data["path"] == folder_path:
            logging.info("[validate_shared_directory] Shared directory found.")
            return True
    logging.error("[validate_shared_directory] Shared directory not found.")
    return False


async def login_nas(ip_address: str) -> str | None:
    config = Config()
    params = LoginNasApi(
        api="SYNO.API.Auth",
        version=3,
        method="login",
        session="FileStation",
        account=config.NAS_USERNAME,
        passwd=config.NAS_PASSWORD,
        format="cookie",
    )
    port = port_matcher(ip_address=ip_address)

    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[login_nas] Login into NAS via API.")
            response = await client.get(NAS_BASE_URL, params=params.model_dump())
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[login_nas] Login failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

            return data["data"]["sid"]
        except NasIntegrationError:
            raise
        except ServicesConnectionError:
            raise
        except Exception as e:
            logging.error(f"[login_nas] Cannot initialize NAS connection: {e}")
        finally:
            await client.aclose()
    return None


async def logout_nas(ip_address: str) -> None:
    params = LogoutNasApi(api="SYNO.API.Auth", version=1, method="logout", session="FileStation")
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"
    async with httpx.AsyncClient() as client:
        try:
            logging.info("[logout_nas] Logout into NAS via API.")
            response = await client.get(NAS_BASE_URL, params=params.model_dump())
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[logout_nas] Logout failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"[logout_nas] Cannot initialize NAS connection: {e}")
        finally:
            await client.aclose()
    return None


async def check_shared_folder_already_exist(connection_id: str, ip_address: str, folder_path: str | list[str]) -> None:
    params = ListShareNasApi(api="SYNO.FileStation.List", version=2, method="list_share", _sid=connection_id)

    port = port_matcher(ip_address=ip_address)

    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("Validate shared folder already on NAS via API.")
            response = await client.get(NAS_BASE_URL, params=params.model_dump())
            response.raise_for_status()
            data = response.json()

            if not data["success"]:
                logging.error("Checking shared folder failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

            folder_path = grab_shared_dir(path=folder_path)
            is_available = validate_shared_directory(data=data, folder_path=folder_path)

            if not is_available:
                raise DataNotFoundError(
                    detail="Shared directory not found. " "Please please ensure shared directory already created on NAS."
                )
        except NasIntegrationError:
            raise
        except DataNotFoundError:
            raise
        except Exception as e:
            logging.error(f"[check_shared_folder_already_exist] Cannot initialize NAS connection: {e}")
        finally:
            await client.aclose()
    return None


async def check_target_dir_already_exist(
    connection_id: str, ip_address: str, shared_folder: str, target_folder: str | list
) -> Union[dict, list[dict]]:
    port = port_matcher(ip_address=ip_address)

    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    if isinstance(target_folder, str):
        target_folder = [target_folder]

    responses = []

    async with httpx.AsyncClient() as client:
        for folder in target_folder:
            params = ListShareNasApi(
                api="SYNO.FileStation.List",
                version=2,
                method="list",
                _sid=connection_id,
                folder_path=f"{shared_folder}/{folder}",
            )
            try:
                logging.info(f"[check_target_dir_already_exist] Checking folder: {folder}")
                response = await client.get(NAS_BASE_URL, params=params.model_dump())
                response.raise_for_status()
                data = response.json()
                responses.append(data)
            except Exception as e:
                logging.error(f"[check_target_dir_already_exist] Error checking folder '{folder}': {e}")
                responses.append({"error": str(e), "folder": folder})

    return responses if len(responses) > 1 else responses[0]


async def create_nas_dir(
    connection_id: str,
    ip_address: str,
    folder_path: str | list[str],
    directory_name: str | list[str],
) -> None:
    params = CreateFolderNasApi(
        api="SYNO.FileStation.CreateFolder",
        version=2,
        method="create",
        folder_path=folder_path,
        name=directory_name,
        _sid=connection_id,
    )

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    payload = params.model_dump()

    if isinstance(folder_path, list):
        payload["folder_path"] = json.dumps(folder_path)
    if isinstance(directory_name, list):
        payload["name"] = json.dumps(directory_name)

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[create_nas_dir] Create directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[create_nas_dir] Creating new NAS directory failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"[create_nas_dir] Error while creating new directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def update_nas_dir(
    connection_id: str,
    ip_address: str,
    folder_path: str | list[str],
    changed_dir_into: str | list[str],
) -> None:
    params = UpdateFolderNasApi(
        api="SYNO.FileStation.Rename",
        version=2,
        method="rename",
        path=folder_path,
        name=changed_dir_into,
        _sid=connection_id,
    )

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    payload = params.model_dump()

    if isinstance(folder_path, list):
        payload["path"] = json.dumps(folder_path)
    if isinstance(changed_dir_into, list):
        payload["name"] = json.dumps(changed_dir_into)

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[update_nas_dir] Update directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[update_nas_dir] Updating existing NAS directory failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"[update_nas_dir] Error while updating directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def delete_nas_dir(
    connection_id: str,
    ip_address: str,
    folder_path: str | list[str],
) -> None:
    params = DeleteFolderNasApi(
        api="SYNO.FileStation.Delete",
        version=2,
        method="start",
        path=folder_path,
        _sid=connection_id,
    )

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    payload = params.model_dump()

    if isinstance(folder_path, list):
        payload["path"] = json.dumps(folder_path)

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[delete_nas_dir] Delete directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[delete_nas_dir] Deleting existing NAS directory failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"[delete_nas_dir] Error while deleting directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def move_nas_dir(
    connection_id: str,
    ip_address: str,
    folder_path: str | list[str],
    dest_folder_path: str | list[str],
) -> None:
    params = MoveFolderNasApi(
        api="SYNO.FileStation.CopyMove",
        version=3,
        method="start",
        path=folder_path,
        dest_folder_path=dest_folder_path,
        _sid=connection_id,
    )

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    payload = params.model_dump()

    if isinstance(folder_path, list):
        payload["path"] = json.dumps(folder_path)
    if isinstance(dest_folder_path, list):
        payload["dest_folder_path"] = json.dumps(dest_folder_path)

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[move_nas_dir] Delete directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error("[move_nas_dir] Moving existing NAS directory failed, please ensure request are appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"[move_nas_dir] Error while deleting directory in NAS: {e}")
        finally:
            await client.aclose()
    return None
