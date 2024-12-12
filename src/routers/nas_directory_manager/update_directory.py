import os
from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import NasDirectoryManagement
from utils.nas.path_extractor import (
    login_nas,
    logout_nas,
    check_shared_folder_already_exist,
    update_nas_dir,
)

router = APIRouter(tags=["Directory Management"])


async def update_nas_directory(schema: NasDirectoryManagement) -> ResponseDefault:
    logging.info("Endpoint Update NAS Directory.")
    response = ResponseDefault()

    if isinstance(schema.folder_path, list):
        if len(schema.folder_path) > 1:
            common_path = os.path.commonpath(schema.folder_path)
            response.message = (
                f"Updated multiple directories on {schema.ip_address}{common_path}"
            )
        elif len(schema.folder_path) == 1:
            old_path = schema.folder_path[0]
            new_path = (
                f"{'/'.join(old_path.split('/')[:-1])}/{schema.directory_name[0]}"
            )
            response.message = f"Updated a directory from {schema.ip_address}{old_path} into {schema.ip_address}{new_path}"
        else:
            response.success = False
            response.message = "No folder paths provided."
    elif isinstance(schema.folder_path, str):
        old_path = schema.folder_path
        new_path = f"{'/'.join(old_path.split('/')[:-1])}/{schema.directory_name}"
        response.message = f"Updated a directory from {schema.ip_address}{old_path} into {schema.ip_address}{new_path}"
    else:
        response.success = False
        response.message = "Invalid folder_path format."

    conn_id = await login_nas(ip_address=schema.ip_address)

    await check_shared_folder_already_exist(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.folder_path,
    )

    await update_nas_dir(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.folder_path,
        changed_dir_into=schema.directory_name,
    )

    await logout_nas(ip_address=schema.ip_address)

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/update-dir",
    endpoint=update_nas_directory,
    summary="Update existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
