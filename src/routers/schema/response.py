from typing import Union
from pydantic import BaseModel


class TaskResultState(BaseModel):
    task_id: str = None
    status: str = None
    result: Union[list, str, dict] = None


class ResponseDefault(BaseModel):
    success: bool = True
    message: str = None
    data: Union[list, str, dict] = None