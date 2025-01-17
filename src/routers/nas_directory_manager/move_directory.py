from utils.logger import logging
from fastapi import APIRouter, status
from utils.nas.validator import PayloadValidator
from utils.custom_error import ServiceError, DiVA
from src.schema.request_format import NasMoveDirectory
from src.schema.response import ResponseDefault, DirectoryStatus
from utils.nas.external import auth_nas, validate_directory, move_nas_dir

router = APIRouter(tags=["Directory Management"])


async def update_nas_directory(schema: NasMoveDirectory) -> ResponseDefault:
    response = ResponseDefault()
    validator = PayloadValidator()

    validator.move_directory(
        target_folder=schema.target_folder, destination_path=schema.dest_folder_path
    )

    try:
        sid = await auth_nas(ip_address=schema.ip_address)

        target_folder_new_dir, target_folder_existing_dir = await validate_directory(
            ip_address=schema.ip_address,
            directory_path=[schema.target_folder]
            if type(schema.target_folder) is str
            else schema.target_folder,
            sid=sid,
        )

        dest_folder_new_dir, dest_folder_existing_dir = await validate_directory(
            ip_address=schema.ip_address,
            directory_path=[schema.dest_folder_path]
            if type(schema.dest_folder_path) is str
            else schema.dest_folder_path,
            sid=sid,
        )

        if target_folder_existing_dir:
            if dest_folder_new_dir:
                response.message = (
                    "Destination folder should be existing directory on NAS."
                )
                response.data = DirectoryStatus(non_existing_folder=dest_folder_new_dir)
            else:
                logging.info("Endpoint move directory NAS.")
                await move_nas_dir(
                    ip_address=schema.ip_address,
                    target_folder=target_folder_existing_dir,
                    dest_folder_path=dest_folder_existing_dir,
                    sid=sid,
                )

                response.message = "Directory successfully moved."
                response.data = DirectoryStatus(
                    folder_already_exist=target_folder_existing_dir
                )
        else:
            response.message = "Target folder should be existing directory on NAS."
            response.data = DirectoryStatus(non_existing_folder=target_folder_new_dir)
    except DiVA:
        raise
    except Exception as e:
        logging.error(f"Error move NAS directory: {e}")
        raise ServiceError(detail="Failed to move NAS directory.", name="DiVA")
    finally:
        await auth_nas(ip_address=schema.ip_address, auth_type="logout")

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/move-dir",
    endpoint=update_nas_directory,
    summary="Move existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
