import os
from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import NasDirectoryManagement
from utils.helper import (
    login_nas,
    logout_nas,
    check_shared_folder_already_exist,
    create_nas_dir,
)

router = APIRouter(tags=["Directory Management"])


async def create_nas_directory(
    schema: NasDirectoryManagement,
) -> ResponseDefault:
    logging.info("Endpoint Create NAS Directory.")
    response = ResponseDefault()

    BASE_PATH = f"{schema.ip_address}{schema.folder_path}"
    message = f"Created new directory in {BASE_PATH}"

    if isinstance(schema.folder_path, list) and len(schema.folder_path) > 1:
        common_path = os.path.commonpath(schema.folder_path)
        message = f"Created multiple directory on {schema.ip_address}{common_path}"
    if isinstance(schema.folder_path, list) and len(schema.folder_path) == 1:
        common_path = os.path.commonpath(schema.folder_path)
        message = f"Created a directory in {schema.ip_address}{common_path}"

    conn_id = await login_nas(ip_address=schema.ip_address)

    await check_shared_folder_already_exist(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.folder_path,
    )
    await create_nas_dir(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.folder_path,
        directory_name=schema.directory_name,
    )
    await logout_nas(ip_address=schema.ip_address)

    response.message = message

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/create-dir",
    endpoint=create_nas_directory,
    summary="Create new directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)