from utils.logger import logging
from fastapi import APIRouter, status
from utils.custom_error import ServiceError, DiVA
from src.schema.request_format import NasUpdateDirectory
from src.schema.response import ResponseDefault, DirectoryStatus
from utils.nas.validator import PathFormatter, PayloadValidator
from utils.nas.external import (
    auth_nas,
    validate_directory,
    update_nas_dir,
)


router = APIRouter(tags=["Directory Management"])


async def update_nas_directory(schema: NasUpdateDirectory) -> ResponseDefault:
    response = ResponseDefault()
    validator = PayloadValidator()
    formatter = PathFormatter()

    validator.update_directory(
        target_folder=schema.target_folder, changed_name_into=schema.changed_name_into
    )

    try:
        sid = await auth_nas(ip_address=schema.ip_address)

        new_dir, existing_dir = await validate_directory(
            ip_address=schema.ip_address,
            directory_path=[schema.target_folder]
            if type(schema.target_folder) is str
            else schema.target_folder,
            sid=sid,
        )

        if not existing_dir:
            """Response given when target folder is not exist on NAS."""
            response.message = "Target folder should be existing directory on NAS."
            response.data = DirectoryStatus(non_existing_folder=new_dir)
            return response

        refactored_path = formatter.refactor_path(
            target_folder=existing_dir,
            folder_name=[schema.changed_name_into]
            if type(schema.changed_name_into) is str
            else schema.changed_name_into,
        )

        new_updated_dir, updated_dir_already_exist = await validate_directory(
            ip_address=schema.ip_address,
            directory_path=refactored_path,
            sid=sid,
        )

        if not new_updated_dir:
            """Response given when target of updated dir already exist on NAS"""
            response.message = "All target folder already exist."
            response.data = DirectoryStatus(
                folder_already_exist=updated_dir_already_exist,
                non_existing_folder=new_updated_dir,
            )
            return response

        output_target_path, output_rename = formatter.validate_and_update_dir_path(
            new_dir=new_updated_dir,
            target_path=[schema.target_folder]
            if type(schema.target_folder) is str
            else schema.target_folder,
            target_rename_path=[schema.changed_name_into]
            if type(schema.changed_name_into) is str
            else schema.changed_name_into,
        )

        logging.info("Endpoint update NAS directory.")
        await update_nas_dir(
            ip_address=schema.ip_address,
            target_folder=output_target_path,
            changed_name_into=output_rename,
            sid=sid,
        )

        """Response given when at least 1 valid data (valid target_folder and changed_name_into its not an existing folder in NAS)"""
        response.message = "Directory renamed successfully."
        response.data = DirectoryStatus(
            folder_already_exist=updated_dir_already_exist,
            non_existing_folder=new_updated_dir,
        )

    except DiVA:
        raise
    except Exception as e:
        logging.error(f"Error update NAS directory: {e}")
        raise ServiceError(detail="Failed to update directory into NAS.", name="DiVA")
    finally:
        await auth_nas(ip_address=schema.ip_address, auth_type="logout")

    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/update-dir",
    endpoint=update_nas_directory,
    summary="Update existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
