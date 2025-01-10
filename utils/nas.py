import httpx
from typing import Optional, Literal
from collections import Counter
from utils.logger import logging
from utils.helper import port_matcher
from src.secret import Config
from src.schema.request_format import (
    ListShareNasApi,
)
from utils.custom_error import (
    NasIntegrationError,
    DataNotFoundError,
    ServicesConnectionError,
)


def path_formatter(shared_folder: list | str, target_folder: list | str) -> list:
    """Ensure shared folder and target folder in same data type."""
    if (isinstance(shared_folder, list) and isinstance(target_folder, str)) or (
        isinstance(shared_folder, str) and isinstance(target_folder, list)
    ):
        raise ValueError(
            f"Shared folder and target folder should be of the same data type, "
            f"shared folder {type(shared_folder)}, target folder {type(target_folder)}."
        )
    """Ensure length of shared folder and target folder are equal."""
    if isinstance(shared_folder, list) and isinstance(target_folder, list):
        if len(shared_folder) != len(target_folder):
            raise ValueError(
                f"Shared folder and target folder length should be equal, "
                f"shared folder: {len(shared_folder)}, target folder: {len(target_folder)}."
            )

        """Ensure target_folder has unique elements"""
        duplicates = [item for item, count in Counter(target_folder).items() if count > 1]
        if duplicates:
            raise ValueError(f"Target folder contains duplicate entries: {duplicates}.")

    """Handle formatter in list data type."""
    if isinstance(shared_folder, list):
        for entry in shared_folder:
            if not entry.startswith("/"):
                raise ValueError(f"Shared folder should start with '/': {entry}.")
        return [entry + "/" + target_folder[idx] for idx, entry in enumerate(shared_folder)]

    """Handle formatter in string data type."""
    if isinstance(shared_folder, str):
        if not shared_folder.startswith("/"):
            raise ValueError(f"Shared folder should start with '/': {shared_folder}.")
        return [shared_folder + "/" + target_folder]


def shared_folder_validator(shared_folder: list, target_shared_folder: list[str] | str) -> None:
    available_paths = {entry["path"] for entry in shared_folder}

    """Ensure all target shared folder startwith '/' in list data type."""
    if isinstance(target_shared_folder, list):
        invalid_list = [target for target in target_shared_folder if not target.startswith("/")]
        if invalid_list:
            raise ValueError(f"Target shared folder should be started with '/', target shared folder: {invalid_list}")

        not_found_shared_dir = [target for target in target_shared_folder if target not in available_paths]
        if not_found_shared_dir:
            raise DataNotFoundError(f"Shared folder {not_found_shared_dir} not found.")

    """Ensure target shared folder startwith '/' in list string type."""
    if isinstance(target_shared_folder, str):
        if not target_shared_folder.startswith("/"):
            raise ValueError(f"Target shared folder should be started with '/', target shared folder: {target_shared_folder}")

        if target_shared_folder not in available_paths:
            raise DataNotFoundError(f"Shared folder '{target_shared_folder}' not found.")

    return None


async def auth_nas(
    ip_address: str,
    auth_type: Literal["login", "logout"] = "login",
) -> Optional[str]:
    config = Config()
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    params = {"api": "SYNO.API.Auth", "version": 3 if auth_type == "login" else 1, "method": auth_type, "session": "FileStation"}

    if auth_type == "login":
        params.update(
            {
                "account": config.NAS_USERNAME,
                "passwd": config.NAS_PASSWORD,
                "format": "cookie",
            }
        )

    async with httpx.AsyncClient() as client:
        try:
            logging.info(f"Performing {auth_type} operation on NAS.")
            response = await client.get(NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data["success"]:
                logging.error(f"{auth_type.capitalize()} failed, please ensure request is appropriate.")
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

            if auth_type == "login":
                return data["data"]["sid"]
        except NasIntegrationError:
            raise
        except ServicesConnectionError:
            raise
        except Exception as e:
            logging.error(f"Cannot complete {auth_type} operation: {e}")
        finally:
            await client.aclose()

    return None


async def validate_directory(ip_address: str, directory_path: list, sid: str) -> tuple[Optional[list], Optional[list]]:
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"
    directory_already_exist = []
    new_directory = []

    async with httpx.AsyncClient() as client:
        try:
            for path in directory_path:
                logging.info(f"Validating path {path}.")
                params = {"api": "SYNO.FileStation.List", "version": 2, "method": "list", "folder_path": path, "_sid": sid}

                response = await client.get(NAS_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                if not data["success"]:
                    logging.info(f"Validated new path {path}.")
                    new_directory.append(path)
                else:
                    logging.warning(f"Path {path} already exist.")
                    directory_already_exist.append(path)
        except NasIntegrationError:
            raise
        except ServicesConnectionError:
            raise
        except Exception as e:
            logging.error(f"Cannot validate dirctory: {e}")
        finally:
            await client.aclose()

    return (new_directory if new_directory else None, directory_already_exist if directory_already_exist else None)


async def validate_shared_folder_already_exist(ip_address: str, sid: str) -> Optional[list]:
    params = ListShareNasApi(api="SYNO.FileStation.List", version=2, method="list_share", _sid=sid)

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

            return data["data"]["shares"]
        except NasIntegrationError:
            raise
        except DataNotFoundError:
            raise
        except Exception as e:
            logging.error(f"[check_shared_folder_already_exist] Cannot initialize NAS connection: {e}")
        finally:
            await client.aclose()
    return None
