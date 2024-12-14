from utils.logger import logging
from fastapi import APIRouter, status, Request
from src.schema.response import ResponseDefault

router = APIRouter(tags=["Classification"])


async def labels_distribution(
    request: Request,
    pages: int = 1,
    extracted_images: int = 50,
    is_validated: bool = False,
) -> ResponseDefault:
    logging.info("Endpoint Labels Distribution.")
    response = ResponseDefault()
    response.message = "Retrieved labels distribution."
    return response


router.add_api_route(
    methods=["GET"],
    path="/classification/distribution",
    endpoint=labels_distribution,
    summary="Retrieve chunked image data for training purposes.",
    status_code=status.HTTP_200_OK,
)
