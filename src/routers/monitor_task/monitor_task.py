from uuid import UUID
from utils.logger import logging
from celery.result import AsyncResult
from fastapi import APIRouter, status
from services.celery.worker import app
from src.schema.response import (
    ResponseDefault,
    TaskResultState,
)

router = APIRouter(tags=["Task Monitor"])


async def monitor_task(
    task_id: UUID,
) -> ResponseDefault:
    logging.info("Endpoint Monitor Task")
    response = ResponseDefault()
    task_state = TaskResultState()

    task_result = AsyncResult(str(task_id), app=app)

    task_state.task_id = str(task_id)
    task_state.status = task_result.status
    task_state.result = task_result.result

    response.message = f"Extracted information {task_id}."
    response.data = task_state
    return response


router.add_api_route(
    methods=["GET"],
    path="/monitor/task-id/{task_id}",
    endpoint=monitor_task,
    summary="Monitor task status and result.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
