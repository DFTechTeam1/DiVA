from collections import Counter
from utils.custom_error import (
    NasIntegrationError,
    DataNotFoundError,
)


def path_formatter(shared_folder: list | str, target_folder: list | str) -> list:
    """Ensure shared folder is filled."""
    if not shared_folder:
        raise NasIntegrationError("Shared folder cannot be empty.")

    """Ensure target folder is filled."""
    if not target_folder:
        raise NasIntegrationError("Target folder cannot be empty.")

    """Ensure shared folder and target folder in same data type."""
    if (isinstance(shared_folder, list) and isinstance(target_folder, str)) or (
        isinstance(shared_folder, str) and isinstance(target_folder, list)
    ):
        raise NasIntegrationError(
            f"Shared folder and target folder should be of the same data type, "
            f"shared folder {type(shared_folder)}, target folder {type(target_folder)}."
        )
    """Ensure length of shared folder and target folder are equal."""
    if isinstance(shared_folder, list) and isinstance(target_folder, list):
        if len(shared_folder) != len(target_folder):
            raise NasIntegrationError(
                f"Shared folder and target folder length should be equal, "
                f"shared folder: {len(shared_folder)}, target folder: {len(target_folder)}."
            )

        """Ensure target_folder has unique elements"""
        duplicates = [item for item, count in Counter(target_folder).items() if count > 1]
        if duplicates:
            raise NasIntegrationError(f"Target folder contains duplicate entries: {duplicates}.")

    """Handle formatter in list data type."""
    if isinstance(shared_folder, list):
        for entry in shared_folder:
            if not entry.startswith("/"):
                raise NasIntegrationError(f"Shared folder should start with '/': {entry}.")
        return [entry + "/" + target_folder[idx] for idx, entry in enumerate(shared_folder)]

    """Handle formatter in string data type."""
    if isinstance(shared_folder, str):
        if not shared_folder.startswith("/"):
            raise NasIntegrationError(f"Shared folder should start with '/': {shared_folder}.")
        return [shared_folder + "/" + target_folder]


def validate_update_dir_path(target_folder: list | str, changed_name_into: list | str) -> None:
    """Ensure shared folder is filled."""
    if not target_folder:
        raise NasIntegrationError("Shared folder cannot be empty.")

    """Ensure target folder is filled."""
    if not changed_name_into:
        raise NasIntegrationError("Target folder cannot be empty.")

    """Ensure shared folder and target folder in same data type."""
    if (isinstance(changed_name_into, list) and isinstance(target_folder, str)) or (
        isinstance(changed_name_into, str) and isinstance(target_folder, list)
    ):
        raise NasIntegrationError(
            f"Target folder and change name into should be of the same data type, "
            f"Target folder {type(target_folder)}, change name into {type(changed_name_into)}."
        )
    """Ensure length of shared folder and target folder are equal."""
    if isinstance(changed_name_into, list) and isinstance(target_folder, list):
        if len(changed_name_into) != len(target_folder):
            raise NasIntegrationError(
                f"Target folder and change name into length should be equal, "
                f"Target folder: {len(target_folder)}, change name into: {len(changed_name_into)}."
            )

        """Ensure target_folder has unique elements"""
        duplicates = [item for item, count in Counter(target_folder).items() if count > 1]
        if duplicates:
            raise NasIntegrationError(f"Target folder contains duplicate entries: {duplicates}.")
    if isinstance(target_folder, str):
        if not target_folder.startswith("/"):
            raise NasIntegrationError(f"Shared folder should start with '/': {target_folder}.")
    return None


def validate_shared_folder(shared_folder: list, target_shared_folder: list[str] | str) -> None:
    available_paths = {entry["path"] for entry in shared_folder}

    """Ensure all target shared folder startwith '/' in list data type."""
    if isinstance(target_shared_folder, list):
        invalid_list = [target for target in target_shared_folder if not target.startswith("/")]
        if invalid_list:
            raise NasIntegrationError(f"Target shared folder should be started with '/', target shared folder: {invalid_list}")

        not_found_shared_dir = [target for target in target_shared_folder if target not in available_paths]
        if not_found_shared_dir:
            raise DataNotFoundError(f"Shared folder {not_found_shared_dir} not found.")

    """Ensure target shared folder startwith '/' in list string type."""
    if isinstance(target_shared_folder, str):
        if not target_shared_folder.startswith("/"):
            raise NasIntegrationError(
                f"Target shared folder should be started with '/', target shared folder: {target_shared_folder}"
            )

        if target_shared_folder not in available_paths:
            raise DataNotFoundError(f"Shared folder '{target_shared_folder}' not found.")
    return None


def decode_path_formatter(paths: list) -> tuple[list, list]:
    """
    Changed into default structures.

    input = ['/apitesting/sub1/sub2']
    output_shared_dir = ['/apitesting']
    output_target_dir = ['sub1/sub2']
    """
    shared_dir = []
    target_dir = []

    for path in paths:
        parts = path.strip("/").split("/", 1)
        shared_dir.append(f"/{parts[0]}")
        target_dir.append(parts[1] if len(parts) > 1 else "")

    return (shared_dir, target_dir)


def refactor_path(target_folder: list, folder_name: list) -> list:
    """
    Changed into new path for validate existing dir.

    input_target_folder = ['/apitesting/sub1/sub2']
    input_folder_name = ['sub3']
    output_path = ['/apitesting/sub1/sub3']
    """

    base_paths = ["/".join(path.split("/")[:-1]) for path in target_folder]
    return [f"{base}/{new}" for base, new in zip(base_paths, folder_name)]


def validate_and_update_dir_path(target_path: list, target_rename_path: list, new_dir: list):
    if len(target_path) != len(target_rename_path):
        raise ValueError("target_path and target_rename_path must have the same length.")

    output_target_path = []
    output_rename = []

    for path, rename in zip(target_path, target_rename_path):
        renamed_path = f"{'/'.join(path.split('/')[:-1])}/{rename}"

        # Check if the renamed path is not in new_dir
        if renamed_path in new_dir:
            output_target_path.append(path)
            output_rename.append(rename)

    return output_target_path, output_rename
