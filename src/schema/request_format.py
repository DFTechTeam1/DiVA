from typing import Literal
from pydantic import BaseModel, Extra


class CategoryDocumentation(BaseModel):
    category: str
    description: str


class IpAddress(BaseModel):
    ip_address: Literal[
        "192.168.100.101",
        "192.168.100.102",
        "192.168.100.103",
        "192.168.100.104",
        "192.168.100.105",
    ]


class AllowedIpAddress(BaseModel):
    ip_address: list = [
        "192.168.100.1",
        "192.168.100.2",
        "192.168.100.3",
        "192.168.100.4",
        "192.168.100.5",
        "192.168.100.6",
        "192.168.100.7",
        "192.168.100.8",
        "192.168.100.9",
        "127.0.0.1",
    ]


class NasDirectoryManagement(IpAddress):
    folder_path: str | list[str]
    directory_name: str | list[str]


class NasDeleteDirectory(IpAddress):
    folder_path: str | list[str]


class NasMoveDirectory(IpAddress):
    path: str | list[str]
    dest_folder_path: str | list[str]


class SynologyApiPath(BaseModel):
    api: Literal[
        "SYNO.API.Auth",
        "SYNO.FileStation.CreateFolder",
        "SYNO.FileStation.Rename",
        "SYNO.FileStation.Delete",
        "SYNO.FileStation.Delete",
        "SYNO.FileStation.List",
        "SYNO.FileStation.CopyMove",
    ]


class SynologyApiVersion(BaseModel):
    version: int


class SynologyMethod(BaseModel):
    method: Literal[
        "login",
        "logout",
        "query",
        "list_share",
        "create",
        "rename",
        "start",
        "status",
    ]


class SynologyApiSession(BaseModel):
    session: Literal["FileStation"]


class NasSidParams(BaseModel):
    _sid: str

    class Config:
        extra = Extra.allow


class LoginNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    SynologyApiSession,
):
    account: str
    passwd: str
    format: Literal["cookie"]


class LogoutNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    SynologyApiSession,
):
    pass


class ListShareNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    pass


class CreateFolderNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    folder_path: str | list[str]
    name: str | list[str]


class UpdateFolderNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    path: str | list[str]
    name: str | list[str]


class DeleteFolderNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    path: str | list[str]


class MoveFolderNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    path: str | list[str]
    dest_folder_path: str | list[str]
    remove_src: bool = True
