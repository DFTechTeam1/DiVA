import logging
from fastapi import APIRouter, status, Request
from src.schema.response import ResponseDefault
from src.schema.request_format import AllowedIpAddress
from utils.custom_errors import AccessUnauthorized
from utils.query.labels_documentation import retrieve_labels_documentation

router = APIRouter(tags=["Classification"])


async def labels_documentation(request: Request) -> ResponseDefault:
    logging.info("Endpoint Labels Documentation.")

    response = ResponseDefault()
    allow_ips = AllowedIpAddress()

    ip_address = request.client.host
    if ip_address not in allow_ips.ip_address:
        raise AccessUnauthorized(
            "IP Address blacklisted. Please ask IT Team for add IP as whitelist."
        )

    docs = await retrieve_labels_documentation()
    response.message = "Retrieved all documentation."
    response.data = docs
    return response


router.add_api_route(
    methods=["GET"],
    path="/classification/label-docs",
    endpoint=labels_documentation,
    summary="Retrieve label documentation.",
    status_code=status.HTTP_200_OK,
)
