from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault, DirectoryStatus
from src.schema.request_format import NasDirectoryManagement
from utils.custom_error import ServiceError, DiVA
from utils.nas.validator import (
    validate_shared_folder,
    path_formatter,
    decode_path_formatter,
)
from utils.nas.external import (
    auth_nas,
    extract_shared_folder,
    validate_directory,
    create_nas_dir,
)

router = APIRouter(tags=["Directory Management"])


async def create_nas_directory_endpoint(schema: NasDirectoryManagement) -> ResponseDefault:
    response = ResponseDefault()

    formated_path = path_formatter(shared_folder=schema.shared_folder, target_folder=schema.target_folder)
    sid = await auth_nas(ip_address=schema.ip_address)
    new_dir, existing_dir = await validate_directory(ip_address=schema.ip_address, directory_path=formated_path, sid=sid)

    try:
        if not new_dir:
            response.message = "Directory already exist."
            response.data = DirectoryStatus(folder_already_exsist=existing_dir)
            return response

        shared_folder = await extract_shared_folder(ip_address=schema.ip_address, sid=sid)
        validate_shared_folder(shared_folder=shared_folder, target_shared_folder=schema.shared_folder)

        logging.info("Endpoint create NAS directory.")
        shared_folder, target_folder = decode_path_formatter(paths=new_dir)
        await create_nas_dir(ip_address=schema.ip_address, shared_folder=shared_folder, target_folder=target_folder, sid=sid)

        response.message = "Directory created successfully."
        response.data = DirectoryStatus(folder_already_exsist=existing_dir)
    except DiVA:
        raise
    except Exception as e:
        logging.error(f"Error create NAS directory: {e}")
        raise ServiceError(detail="Failed to create directory into NAS.", name="DiVA")
    finally:
        await auth_nas(ip_address=schema.ip_address, auth_type="logout")

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/create-dir",
    endpoint=create_nas_directory_endpoint,
    summary="Create new directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
