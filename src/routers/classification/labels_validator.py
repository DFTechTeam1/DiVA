from utils.logger import logging
from fastapi import APIRouter, status, Request
from src.schema.response import ResponseDefault
from src.schema.request_format import LabelsValidator, AllowedIpAddress
from utils.query.labels_validator import update_labels
from utils.custom_errors import AccessUnauthorized

router = APIRouter(tags=["Classification"])


async def labels_validator(
    request: Request, schema: LabelsValidator
) -> ResponseDefault:
    logging.info("Endpoint Labels Validator.")

    response = ResponseDefault()
    allow_ips = AllowedIpAddress()

    ip_address = request.client.host
    if ip_address not in allow_ips.ip_address:
        raise AccessUnauthorized(
            "IP Address blacklisted. Please ask IT Team for add IP as whitelist."
        )

    await update_labels(
        image_id=schema.image_id,
        ip_address=ip_address,
        artifacts=schema.artifacts,
        nature=schema.nature,
        living_beings=schema.living_beings,
        natural=schema.natural,
        manmade=schema.manmade,
        conceptual=schema.conceptual,
        art_deco=schema.art_deco,
        architectural=schema.architectural,
        artistic=schema.artistic,
        sci_fi=schema.sci_fi,
        fantasy=schema.fantasy,
        day=schema.day,
        afternoon=schema.afternoon,
        evening=schema.evening,
        night=schema.night,
        warm=schema.warm,
        cool=schema.cool,
        neutral=schema.neutral,
        gold=schema.gold,
        asian=schema.asian,
        european=schema.european,
    )

    response.message = f"Entry {schema.image_id} validated."
    return response


router.add_api_route(
    methods=["PATCH"],
    path="/classification/label-validator",
    endpoint=labels_validator,
    summary="Validate image labels.",
    status_code=status.HTTP_200_OK,
)
