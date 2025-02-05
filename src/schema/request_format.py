from enum import StrEnum
from typing import Literal
from pydantic import BaseModel, Extra, Field


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
    folder_path: str | list[str] = None
    directory_name: str | list[str] = None


class NasDeleteDirectory(IpAddress):
    folder_path: str | list[str] = None


class NasMoveDirectory(IpAddress):
    path: str | list[str] = None
    dest_folder_path: str | list[str] = None


class LabelsValidator(BaseModel):
    image_id: int = Field(
        default=None, ge=1, description="Image ID must be greater than or equal to 1"
    )
    artifacts: bool = False
    nature: bool = False
    living_beings: bool = False
    natural: bool = False
    manmade: bool = False
    conceptual: bool = False
    art_deco: bool = False
    heaven: bool = False
    architectural: bool = False
    artistic: bool = False
    sci_fi: bool = False
    fantasy: bool = False
    day: bool = False
    afternoon: bool = False
    evening: bool = False
    night: bool = False
    warm: bool = False
    cool: bool = False
    neutral: bool = False
    gold: bool = False
    asian: bool = False
    european: bool = False


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
    version: int = None


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
    account: str = None
    passwd: str = None
    format: Literal["cookie"] = None


class LogoutNasApi(
    SynologyApiPath, SynologyApiVersion, SynologyMethod, SynologyApiSession
):
    pass


class ListShareNasApi(
    SynologyApiPath, SynologyApiVersion, SynologyMethod, NasSidParams
):
    pass


class CreateFolderNasApi(
    SynologyApiPath, SynologyApiVersion, SynologyMethod, NasSidParams
):
    folder_path: str | list[str] = None
    name: str | list[str] = None


class UpdateFolderNasApi(
    SynologyApiPath, SynologyApiVersion, SynologyMethod, NasSidParams
):
    path: str | list[str] = None
    name: str | list[str] = None


class DeleteFolderNasApi(
    SynologyApiPath, SynologyApiVersion, SynologyMethod, NasSidParams
):
    path: str | list[str] = None


class MoveFolderNasApi(
    SynologyApiPath,
    SynologyApiVersion,
    SynologyMethod,
    NasSidParams,
):
    path: str | list[str] = None
    dest_folder_path: str | list[str] = None
    remove_src: bool = True


class ModelType(StrEnum):
    classification: str = "classification"
    query: str = "query"
