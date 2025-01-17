from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault, DirectoryStatus
from src.schema.request_format import NasDirectoryManagement
from utils.custom_error import ServiceError, DiVA
from utils.nas.validator import PayloadValidator, PathFormatter
from utils.nas.external import (
    auth_nas,
    create_nas_dir,
    extract_shared_folder,
    validate_directory,
)

router = APIRouter(tags=["Directory Management"])


async def create_nas_directory_endpoint(
    schema: NasDirectoryManagement,
) -> ResponseDefault:
    response = ResponseDefault()
    validator = PayloadValidator()
    formatter = PathFormatter()

    validator.create_directory(
        shared_folder=schema.shared_folder, target_folder=schema.target_folder
    )
    formated_path = formatter.merge_path(
        shared_folder=schema.shared_folder, target_folder=schema.target_folder
    )

    try:
        sid = await auth_nas(ip_address=schema.ip_address)

        new_dir, existing_dir = await validate_directory(
            ip_address=schema.ip_address, directory_path=formated_path, sid=sid
        )

        if not new_dir:
            response.message = "Directory already exist."
            response.data = DirectoryStatus(folder_already_exsist=existing_dir)
            return response

        shared_folder = await extract_shared_folder(
            ip_address=schema.ip_address, sid=sid
        )
        validator.shared_folder(
            actual_shared_folder=shared_folder,
            target_shared_folder=schema.shared_folder,
        )

        shared_folder, target_folder = formatter.revoke_path(path=new_dir)

        logging.info("Endpoint create directory NAS.")
        await create_nas_dir(
            ip_address=schema.ip_address,
            shared_folder=shared_folder,
            target_folder=target_folder,
            sid=sid,
        )

        response.message = "Directory created successfully."
        response.data = DirectoryStatus(
            folder_already_exsist=existing_dir, non_existing_folder=new_dir
        )
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
