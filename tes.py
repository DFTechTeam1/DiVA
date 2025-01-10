# def validate_directories(data_1: dict, data_2: list) -> None:
#     # Extract all paths from data_1
#     existing_paths = {share["path"] for share in data_1["shares"]}

#     # Find missing directories
#     missing_dirs = [directory for directory in data_2 if directory not in existing_paths]

#     if missing_dirs:
#         raise ValueError(f"The following directories are missing: {missing_dirs}")

#     print("All directories in data_2 exist in data_1.")

# # # Example Data
# data_1 = [
#         {"isdir": True, "name": "3FEB-SF", "path": "/3FEB-SF"},
#         {"isdir": True, "name": "apitesting", "path": "/apitesting"},
#         {"isdir": True, "name": "CLIENT_PREVIEW", "path": "/CLIENT_PREVIEW"},
#         {"isdir": True, "name": "Dfactory", "path": "/Dfactory"},
#         {"isdir": True, "name": "docker", "path": "/docker"},
#         {"isdir": True, "name": "home", "path": "/home"},
#         {"isdir": True, "name": "homes", "path": "/homes"},
#         {"isdir": True, "name": "photo", "path": "/photo"},
#         {"isdir": True, "name": "RHGA - All Files", "path": "/RHGA - All Files"},
#         {"isdir": True, "name": "web", "path": "/web"},
#         {"isdir": True, "name": "web_packages", "path": "/web_packages"},
#     ]


# data_2 = ["/Dfactory", "/web", "/random", "anjayyy"]

# # Run validation
# try:
#     validate_directories(data_1, data_2)
# except ValueError as e:
#     print(e)


# print(json.dumps(data_2))

import asyncio
from utils.nas import auth_nas, validate_shared_folder_already_exist, shared_folder_validator


async def main():
    # TODO: create validation for only creating dir based on new_dir variable
    target_shared_folder = ["Dfactdaory"]
    # target_folder = ["random", "anjay"]
    # formated_path = path_formatter(shared_folder=shared_folder, target_folder=target_folder)
    sid = await auth_nas(ip_address="192.168.100.105")
    shared_folder = await validate_shared_folder_already_exist(ip_address="192.168.100.105", sid=sid)
    shared_folder_validator(shared_folder=shared_folder, target_shared_folder=target_shared_folder)
    # new_dir, existing_dir = await validate_directory(ip_address="192.168.100.105", directory_path=formated_path, sid=sid)
    # print(new_dir)
    # print(existing_dir)


asyncio.run(main())
