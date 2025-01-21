from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from services.celery.tasks import train_finetune_custom_resnet50
from src.schema.response import (
    TaskResultState,
)

router = APIRouter(tags=["Enrich Knowledge"])


async def labels_documentation() -> ResponseDefault:
    logging.info("Endpoint Enrich Knowledge.")

    response = ResponseDefault()
    task_state = TaskResultState()

    logging.info("Initiate model development task.")
    task = train_finetune_custom_resnet50.delay()

    task_state.task_id = task.id

    response.message = "Initialized encoder task."
    response.data = task_state
    return response


router.add_api_route(
    methods=["POST"],
    path="/train-models",
    endpoint=labels_documentation,
    summary="Training and finetuned inhouse ResNet50.",
    status_code=status.HTTP_200_OK,
)
