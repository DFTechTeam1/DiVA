from utils.logger import logging
from fastapi import APIRouter, status, Request, Query
from src.schema.response import ResponseDefault
from utils.query.pagination import extract_distributed_entries

router = APIRouter(tags=["Classification"])


async def labels_distribution(
    request: Request,
    page: int = Query(default=1, ge=1),
    image_per_page: int = Query(default=10, ge=1),
    is_validated: bool = False,
) -> ResponseDefault:
    logging.info("Endpoint Labels Distribution.")
    response = ResponseDefault()
    ip_address = request.client.host
    tes = await extract_distributed_entries(
        page=page,
        image_per_page=image_per_page,
        ip_address=ip_address,
        is_validated=is_validated,
    )
    response.message = "Retrieved labels distribution."
    response.data = tes
    return response


router.add_api_route(
    methods=["GET"],
    path="/classification/distribution",
    endpoint=labels_distribution,
    summary="Retrieve chunked image data for training purposes.",
    status_code=status.HTTP_200_OK,
)
