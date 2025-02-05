from utils.logger import logging
from fastapi import APIRouter, status, Request, Query
from src.schema.response import ResponseDefault
from src.schema.request_format import AllowedIpAddress
from utils.custom_errors import AccessUnauthorized
from utils.query.pagination import extract_distributed_entries

router = APIRouter(tags=["Classification"])


async def labels_distribution(
    request: Request,
    page: int = Query(
        default=1, ge=1, description="Total page available for current chunk data."
    ),
    image_per_page: int = Query(
        default=10, ge=1, description="Splitted total image into current chunk data."
    ),
    is_validated: bool = False,
) -> ResponseDefault:
    logging.info("Endpoint Labels Distribution.")

    response = ResponseDefault()
    allow_ips = AllowedIpAddress()

    ip_address = request.client.host
    if ip_address not in allow_ips.ip_address:
        raise AccessUnauthorized(
            "IP Address blacklisted. Please ask IT Team for add IP as whitelist."
        )

    pagination = await extract_distributed_entries(
        page=page,
        image_per_page=image_per_page,
        ip_address=ip_address,
        is_validated=is_validated,
    )
    response.message = "Retrieved labels distribution."
    response.data = pagination
    return response


router.add_api_route(
    methods=["GET"],
    path="/classification/label-distribution",
    endpoint=labels_distribution,
    summary="Retrieve chunked image entries.",
    status_code=status.HTTP_200_OK,
)
