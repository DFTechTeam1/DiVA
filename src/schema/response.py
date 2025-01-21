from typing import Optional, Any
from pydantic import BaseModel


class Pagination(BaseModel):
    available_page: int = None
    images: list = None


class DirectoryStatus(BaseModel):
    folder_already_exist: Optional[list] = None
    non_existing_folder: Optional[list] = None


class TaskResultState(BaseModel):
    task_id: str = None
    status: str = None
    result: Optional[Any] = None


class ResponseDefault(BaseModel):
    success: bool = True
    message: str = None
    data: Optional[Any] = None
