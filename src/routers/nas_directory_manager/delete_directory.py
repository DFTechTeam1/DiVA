from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault, DirectoryStatus
from src.schema.request_format import NasDeleteDirectory
from utils.custom_error import ServiceError, DiVA
from utils.nas.external import (
    auth_nas,
    validate_directory,
    delete_nas_dir,
)

router = APIRouter(tags=["Directory Management"])


async def delete_nas_directory_endpoint(schema: NasDeleteDirectory) -> ResponseDefault:
    response = ResponseDefault()

    sid = await auth_nas(ip_address=schema.ip_address)
    new_dir, existing_dir = await validate_directory(
        ip_address=schema.ip_address,
        directory_path=[schema.target_folder] if type(schema.target_folder) is str else schema.target_folder,
        sid=sid,
    )
    try:
        if not existing_dir:
            response.message = "Input should be existing directory on NAS."
            response.data = DirectoryStatus(non_existing_folder=new_dir)
            return response

        logging.info("Endpoint delete NAS directory.")
        await delete_nas_dir(ip_address=schema.ip_address, folder_path=existing_dir, sid=sid)

        response.message = "Directory successfully removed."
        response.data = DirectoryStatus(non_existing_folder=new_dir, folder_already_exsist=existing_dir)
    except DiVA:
        raise
    except ValueError:
        raise
    except Exception as e:
        logging.error(f"Error delete NAS directory: {e}")
        raise ServiceError(detail="Failed to delete directory into NAS.", name="DiVA")
    finally:
        await auth_nas(ip_address=schema.ip_address, auth_type="logout")

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/delete-dir",
    endpoint=delete_nas_directory_endpoint,
    summary="Delete existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
