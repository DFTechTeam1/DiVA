from typing import Annotated
from utils.logger import logging
from fastapi import APIRouter, status, Request, Depends
from services.postgres.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.response import ResponseDefault
from src.schema.request_format import LabelsValidator, AllowedIpAddress
from utils.query.general import find_record, update_record
from services.postgres.models import ImageTag
from utils.custom_errors import AccessUnauthorized, ServiceError, DatabaseQueryError, DataNotFoundError, DiVA


router = APIRouter(tags=["Classification"], prefix="/classification")


async def labels_validator(
    request: Request,
    schema: LabelsValidator,
    db: Annotated[AsyncSession, Depends(get_db)],
    image_id: int,
) -> ResponseDefault:
    logging.info("Endpoint Labels Validator.")

    response = ResponseDefault()
    allow_ips = AllowedIpAddress()
    ip_address = request.client.host
    image_record = await find_record(db=db, table=ImageTag, id=image_id, ip_address=ip_address)

    try:
        if ip_address not in allow_ips.ip_address:
            raise AccessUnauthorized("IP Address blacklisted. Please ask IT Team for add IP as whitelist.")

        if not image_record:
            raise DataNotFoundError(detail="Data not found.")

        await update_record(
            db=db,
            table=ImageTag,
            conditions={"id": image_id, "ip_address": ip_address},
            data={
                "artifacts": schema.artifacts,
                "nature": schema.nature,
                "living_beings": schema.living_beings,
                "natural": schema.natural,
                "manmade": schema.manmade,
                "conceptual": schema.conceptual,
                "art_deco": schema.art_deco,
                "architectural": schema.architectural,
                "artistic": schema.artistic,
                "sci_fi": schema.sci_fi,
                "fantasy": schema.fantasy,
                "day": schema.day,
                "afternoon": schema.afternoon,
                "evening": schema.evening,
                "night": schema.night,
                "warm": schema.warm,
                "cool": schema.cool,
                "neutral": schema.neutral,
                "gold": schema.gold,
                "asian": schema.asian,
                "european": schema.european,
                "is_validated": True,
            },
        )
        response.message = f"Entry {image_id} validated."

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        raise ServiceError(detail=f"Service error: {e}.", name="DiVA")
    return response


router.add_api_route(
    methods=["PATCH"],
    path="/validator/{image_id}",
    endpoint=labels_validator,
    summary="Validate image labels.",
    status_code=status.HTTP_200_OK,
)
