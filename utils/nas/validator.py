from collections import Counter
from typing import Any
from utils.custom_error import (
    NasIntegrationError,
    DataNotFoundError,
)


class BaseValidator:
    @staticmethod
    def is_filled(**kwargs: Any) -> NasIntegrationError:
        for name, value in kwargs.items():
            if not value:
                raise NasIntegrationError(f"{name} cannot be empty.")

    @staticmethod
    def is_same_datatype(**kwargs) -> NasIntegrationError:
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        for i in range(len(values) - 1):
            if not isinstance(values[i], type(values[i + 1])):
                raise NasIntegrationError(
                    f"{keys[i]} and {keys[i + 1]} must be of the same data type, "
                    f"{keys[i]}: {type(values[i])}, {keys[i + 1]}: {type(values[i + 1])}."
                )

    @staticmethod
    def is_unique(**kwargs: Any) -> NasIntegrationError:
        for name, elements in kwargs.items():
            duplicates = [
                item for item, count in Counter(elements).items() if count > 1
            ]
            if duplicates:
                raise NasIntegrationError(
                    f"{name} should be unique. Duplicated entries: {duplicates}."
                )

    @staticmethod
    def is_started_with_slash(**kwargs: Any) -> NasIntegrationError:
        for name, value in kwargs.items():
            if isinstance(value, list):
                for entry in value:
                    if not entry.startswith("/"):
                        raise NasIntegrationError(
                            f"{name} should start with '/': {entry}."
                        )
            else:
                if not value.startswith("/"):
                    raise NasIntegrationError(f"{name} should start with '/': {value}.")

    @staticmethod
    def is_length_equal(**kwargs) -> NasIntegrationError:
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        for i in range(len(values) - 1):
            if len(values[i]) != len(values[i + 1]):
                raise NasIntegrationError(
                    f"{keys[i]} and {keys[i + 1]} must have the same length, "
                    f"{keys[i]}: {len(values[i])}, {keys[i + 1]}: {len(values[i + 1])}."
                )


class PayloadValidator(BaseValidator):
    @staticmethod
    def shared_folder(
        actual_shared_folder: list, target_shared_folder: list | str
    ) -> None:
        available_paths = {entry["path"] for entry in actual_shared_folder}

        if isinstance(target_shared_folder, list):
            not_found_shared_dir = [
                target
                for target in target_shared_folder
                if target not in available_paths
            ]
            if not_found_shared_dir:
                raise DataNotFoundError(
                    f"Shared folder {not_found_shared_dir} not found."
                )

        if isinstance(target_shared_folder, str):
            if target_shared_folder not in available_paths:
                raise DataNotFoundError(
                    f"Shared folder '{target_shared_folder}' not found."
                )

    @staticmethod
    def create_directory(
        shared_folder: list | str, target_folder: list | str
    ) -> NasIntegrationError:
        PayloadValidator.is_filled(
            shared_folder=shared_folder, target_folder=target_folder
        )
        PayloadValidator.is_same_datatype(
            shared_folder=shared_folder, target_folder=target_folder
        )
        PayloadValidator.is_started_with_slash(shared_folder=shared_folder)

        if isinstance(target_folder, list):
            PayloadValidator.is_unique(target_folder=target_folder)

        if isinstance(shared_folder, list) and isinstance(target_folder, list):
            PayloadValidator.is_length_equal(
                shared_folder=shared_folder, target_folder=target_folder
            )

    @staticmethod
    def delete_directory(target_folder: list | str) -> NasIntegrationError:
        PayloadValidator.is_filled(target_folder=target_folder)
        PayloadValidator.is_started_with_slash(target_folder=target_folder)
        if isinstance(target_folder, list):
            PayloadValidator.is_unique(target_folder=target_folder)

    @staticmethod
    def move_directory(
        target_folder: list | str, destination_path: list | str
    ) -> NasIntegrationError:
        PayloadValidator.is_filled(
            target_folder=target_folder, destination_path=destination_path
        )
        PayloadValidator.is_same_datatype(
            target_folder=target_folder, destination_path=destination_path
        )
        PayloadValidator.is_started_with_slash(target_folder=target_folder)
        PayloadValidator.is_started_with_slash(destination_path=destination_path)

        if isinstance(target_folder, list):
            PayloadValidator.is_unique(target_folder=target_folder)

        if isinstance(target_folder, list) and isinstance(destination_path, list):
            PayloadValidator.is_length_equal(
                target_folder=target_folder, destination_path=destination_path
            )

    @staticmethod
    def update_directory(
        target_folder: list | str, changed_name_into: list | str
    ) -> NasIntegrationError:
        PayloadValidator.is_filled(
            target_folder=target_folder, changed_name_into=changed_name_into
        )
        PayloadValidator.is_same_datatype(
            target_folder=target_folder, changed_name_into=changed_name_into
        )
        PayloadValidator.is_started_with_slash(target_folder=target_folder)

        if isinstance(target_folder, list):
            PayloadValidator.is_unique(target_folder=target_folder)

        if isinstance(target_folder, list) and isinstance(changed_name_into, list):
            PayloadValidator.is_length_equal(
                target_folder=target_folder, changed_name_into=changed_name_into
            )


class PathFormatter:
    @staticmethod
    def merge_path(shared_folder: list | str, target_folder: list | str) -> list:
        if isinstance(shared_folder, list):
            for entry in shared_folder:
                if not entry.startswith("/"):
                    raise NasIntegrationError(
                        f"Shared folder should start with '/': {entry}."
                    )
            return [
                entry + "/" + target_folder[idx]
                for idx, entry in enumerate(shared_folder)
            ]

        if isinstance(shared_folder, str):
            if not shared_folder.startswith("/"):
                raise NasIntegrationError(
                    f"Shared folder should start with '/': {shared_folder}."
                )
            return [shared_folder + "/" + target_folder]

    @staticmethod
    def revoke_path(path: list) -> tuple[list, list]:
        """
        Changed into default structures.

        input = ['/apitesting/sub1/sub2']
        output_shared_dir = ['/apitesting']
        output_target_dir = ['sub1/sub2']
        """
        shared_dir = []
        target_dir = []

        for entry in path:
            parts = entry.strip("/").split("/", 1)
            shared_dir.append(f"/{parts[0]}")
            target_dir.append(parts[1] if len(parts) > 1 else "")

        return (shared_dir, target_dir)

    @staticmethod
    def refactor_path(target_folder: list, folder_name: list) -> list:
        """
        Changed into new path for validate existing dir.

        input_target_folder = ['/apitesting/sub1/sub2']
        input_folder_name = ['sub3']
        output_path = ['/apitesting/sub1/sub3']
        """

        base_paths = ["/".join(path.split("/")[:-1]) for path in target_folder]
        return [f"{base}/{new}" for base, new in zip(base_paths, folder_name)]

    @staticmethod
    def validate_and_update_dir_path(
        target_path: list, target_rename_path: list, new_dir: list
    ):
        if len(target_path) != len(target_rename_path):
            raise ValueError(
                "target_path and target_rename_path must have the same length."
            )

        output_target_path = []
        output_rename = []

        for path, rename in zip(target_path, target_rename_path):
            renamed_path = f"{'/'.join(path.split('/')[:-1])}/{rename}"

            # Check if the renamed path is not in new_dir
            if renamed_path in new_dir:
                output_target_path.append(path)
                output_rename.append(rename)

        return output_target_path, output_rename
