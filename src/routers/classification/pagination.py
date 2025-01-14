from utils.logger import logging
from urllib.parse import quote
from fastapi import APIRouter, status, Request, Query
from src.schema.response import ResponseDefault
from src.schema.request_format import AllowedIpAddress
from utils.custom_error import AccessUnauthorized
from utils.query.pagination import extract_distributed_entries
from utils.custom_error import ServiceError, DiVA

router = APIRouter(tags=["Classification"], prefix="/classification")


async def labels_distribution(
    request: Request,
    page: int = Query(default=1, ge=1, description="Total page available for current chunk data."),
    image_per_page: int = Query(default=10, ge=1, description="Splitted total image into current chunk data."),
    is_validated: bool = False,
) -> ResponseDefault:
    logging.info("Endpoint Labels Distribution.")

    response = ResponseDefault()
    allow_ips = AllowedIpAddress()
    ip_address = request.client.host

    try:
        if ip_address not in allow_ips.ip_address:
            raise AccessUnauthorized("IP Address blacklisted. Please ask IT Team for add IP as whitelist.")

        pagination = await extract_distributed_entries(
            page=page,
            image_per_page=image_per_page,
            ip_address=ip_address,
            is_validated=is_validated,
        )

        for image in pagination.images:
            relative_path = image["filepath"].replace("/home/dfactory/Project/utils/diva/client_preview/", "", 1)
            image["filepath"] = f"http://localhost:8000/api/v1/images/{quote(relative_path)}"

        response.message = "Retrieved labels distribution."
        response.data = pagination
    except DiVA:
        raise
    except Exception as e:
        raise ServiceError(detail=f"Service error: {e}.", name="DiVA")
    return response


router.add_api_route(
    methods=["GET"],
    path="/paginate",
    endpoint=labels_distribution,
    summary="Retrieve chunked image entries.",
    status_code=status.HTTP_200_OK,
)
