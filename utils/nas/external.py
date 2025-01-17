import httpx
import json
from typing import Optional, Literal
from utils.logger import logging
from utils.helper import port_matcher
from src.secret import Config
from utils.custom_error import (
    NasIntegrationError,
    DataNotFoundError,
    ServicesConnectionError,
)


async def auth_nas(
    ip_address: str,
    auth_type: Literal["login", "logout"] = "login",
) -> Optional[str]:
    config = Config()
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    params = {
        "api": "SYNO.API.Auth",
        "version": 3 if auth_type == "login" else 1,
        "method": auth_type,
        "session": "FileStation",
    }

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
                logging.error(
                    f"{auth_type.capitalize()} failed, please ensure request is appropriate."
                )
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


async def validate_directory(
    ip_address: str, directory_path: list, sid: str
) -> tuple[Optional[list], Optional[list]]:
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"
    directory_already_exist = []
    new_directory = []

    async with httpx.AsyncClient() as client:
        try:
            for path in directory_path:
                logging.info(f"Validating path {path}.")
                params = {
                    "api": "SYNO.FileStation.List",
                    "version": 2,
                    "method": "list",
                    "folder_path": path,
                    "_sid": sid,
                }

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

    return (
        new_directory if new_directory else None,
        directory_already_exist if directory_already_exist else None,
    )


async def extract_shared_folder(ip_address: str, sid: str) -> Optional[list]:
    params = {
        "api": "SYNO.FileStation.List",
        "version": 2,
        "method": "list_share",
        "_sid": sid,
    }

    port = port_matcher(ip_address=ip_address)

    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("Validate shared folder already on NAS via API.")
            response = await client.get(NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data["success"]:
                logging.error(
                    "Checking shared folder failed, please ensure request are appropriate."
                )
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

            return data["data"]["shares"]
        except NasIntegrationError:
            raise
        except DataNotFoundError:
            raise
        except Exception as e:
            logging.error(
                f"[check_shared_folder_already_exist] Cannot initialize NAS connection: {e}"
            )
        finally:
            await client.aclose()
    return None


async def create_nas_dir(
    ip_address: str,
    shared_folder: list[str],
    target_folder: list[str],
    sid: str,
) -> None:
    params = {
        "api": "SYNO.FileStation.CreateFolder",
        "version": 2,
        "method": "create",
        "folder_path": json.dumps(shared_folder),
        "name": json.dumps(target_folder),
        "_sid": sid,
    }

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("Create directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error(
                    "Creating new NAS directory failed, please ensure request are appropriate."
                )
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"Error while creating new directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def delete_nas_dir(
    ip_address: str,
    folder_path: list[str],
    sid: str,
) -> None:
    params = {
        "api": "SYNO.FileStation.Delete",
        "version": 2,
        "method": "start",
        "path": json.dumps(folder_path),
        "_sid": sid,
    }

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("[delete_nas_dir] Delete directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error(
                    "Deleting existing NAS directory failed, please ensure request are appropriate."
                )
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"Error while deleting directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def update_nas_dir(
    ip_address: str,
    target_folder: list[str],
    changed_name_into: list[str],
    sid: str,
) -> None:
    params = {
        "api": "SYNO.FileStation.Rename",
        "version": 2,
        "method": "rename",
        "path": json.dumps(target_folder),
        "name": json.dumps(changed_name_into),
        "_sid": sid,
    }

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("Update directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error(
                    "Updating existing NAS directory failed, please ensure request are appropriate."
                )
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"Error while updating directory in NAS: {e}")
        finally:
            await client.aclose()
    return None


async def move_nas_dir(
    ip_address: str,
    target_folder: list[str],
    dest_folder_path: list[str],
    sid: str,
) -> None:
    params = {
        "api": "SYNO.FileStation.CopyMove",
        "version": 3,
        "method": "start",
        "path": json.dumps(target_folder),
        "dest_folder_path": json.dumps(dest_folder_path),
        "remove_src": True,
        "_sid": sid,
    }

    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/entry.cgi"

    async with httpx.AsyncClient() as client:
        try:
            logging.info("Delete directory via NAS API.")
            response = await client.get(url=NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logging.error(
                    "Moving existing NAS directory failed, please ensure request are appropriate."
                )
                error_detail = data.get("error", {})
                raise NasIntegrationError(detail=error_detail)

        except NasIntegrationError:
            raise
        except Exception as e:
            logging.error(f"Error while moving NAS directory: {e}")
        finally:
            await client.aclose()
    return None


async def list_existing_directory(
    ip_address: str, directory_path: str, sid: str
) -> Optional[list]:
    port = port_matcher(ip_address=ip_address)
    NAS_BASE_URL = f"http://{ip_address}:{port}/webapi/auth.cgi"
    params = {
        "api": "SYNO.FileStation.List",
        "version": 2,
        "method": "list",
        "folder_path": directory_path,
        "_sid": sid,
    }

    async with httpx.AsyncClient() as client:
        try:
            logging.info(f"Validating path {directory_path}.")
            response = await client.get(NAS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            return data["data"]["files"]
        except NasIntegrationError:
            raise
        except ServicesConnectionError:
            raise
        except Exception as e:
            logging.error(f"Cannot validate dirctory: {e}")
        finally:
            await client.aclose()

    return None


async def list_folder(ip_address: str, directory_path: str) -> dict:
    """Used as api testing"""
    try:
        sid = await auth_nas(ip_address=ip_address)
        existing_dir = await list_existing_directory(
            ip_address=ip_address, directory_path=directory_path, sid=sid
        )
    finally:
        await auth_nas(ip_address=ip_address)
    return existing_dir
