from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from utils.query.labels_documentation import retrieve_labels_documentation

router = APIRouter(tags=["Classification"])


async def labels_documentation() -> ResponseDefault:
    logging.info("Endpoint Labels Documentation.")
    response = ResponseDefault()
    docs = await retrieve_labels_documentation()
    response.message = "Retrieved all documentation."
    response.data = docs
    return response


router.add_api_route(
    methods=["GET"],
    path="/classification/docs",
    endpoint=labels_documentation,
    summary="Retrieve label documentation.",
    status_code=status.HTTP_200_OK,
)
