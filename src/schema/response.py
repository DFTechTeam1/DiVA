from typing import Union, Optional
from pydantic import BaseModel


class Pagination(BaseModel):
    available_page: int = None
    images: list = None


class TaskResultState(BaseModel):
    task_id: str = None
    status: str = None
    result: Union[list, str, dict] = None


class ResponseDefault(BaseModel):
    success: bool = True
    message: str = None
    data: Union[dict, list, str, Optional[Pagination], Optional[TaskResultState]] = None
