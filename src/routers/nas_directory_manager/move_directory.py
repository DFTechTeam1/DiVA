import os
from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import (
    NasMoveDirectory,
)
from utils.helper import (
    login_nas,
    logout_nas,
    check_shared_folder_already_exist,
    move_nas_dir,
)

router = APIRouter(tags=["Directory Management"])


async def update_nas_directory(
    schema: NasMoveDirectory,
) -> ResponseDefault:
    logging.info("Endpoint Update NAS Directory.")
    response = ResponseDefault()

    if isinstance(schema.path, list):
        if len(schema.path) > 1:
            from_path = os.path.commonpath(schema.path)
            target_path = os.path.commonpath(schema.dest_folder_path)
            response.message = f"Moved multiple directories from {schema.ip_address}{from_path} into {schema.ip_address}{target_path}"
        elif len(schema.path) == 1:
            old_path = schema.path[0]
            response.message = f"Moved a directory from {schema.ip_address}{old_path} into {schema.ip_address}{schema.dest_folder_path[0]}"
        else:
            response.success = False
            response.message = "No folder paths provided."
    elif isinstance(schema.path, str):
        old_path = schema.path
        response.message = f"Moved a directory from {schema.ip_address}{old_path} into {schema.ip_address}{schema.dest_folder_path}"
    else:
        response.success = False
        response.message = "Invalid folder_path format."

    conn_id = await login_nas(ip_address=schema.ip_address)

    await check_shared_folder_already_exist(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.path,
    )

    await move_nas_dir(
        connection_id=conn_id,
        ip_address=schema.ip_address,
        folder_path=schema.path,
        dest_folder_path=schema.dest_folder_path,
    )

    await logout_nas(ip_address=schema.ip_address)

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/move-dir",
    endpoint=update_nas_directory,
    summary="Move existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)