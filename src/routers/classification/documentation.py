from utils.logger import logging
from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.postgres.connection import get_db
from src.schema.response import ResponseDefault
from src.schema.request_format import AllowedIpAddress
from utils.query.general import find_record
from utils.custom_error import (
    AccessUnauthorized,
    ServiceError,
    DatabaseQueryError,
    DiVA,
)
from services.postgres.models import (
    CategoryDataDocumentation,
    ObjectDocumentationDetails,
    EnvironmentDocumentationDetails,
    DesignTypeDocumentationDetails,
    TimePeriodDocumentationDetails,
    DominantColorDocumentationDetails,
    CultureStyleDocumentationDetails,
)

router = APIRouter(tags=["Classification"], prefix="/classification")


async def labels_documentation(
    request: Request, db: Annotated[AsyncSession, Depends(get_db)]
) -> ResponseDefault:
    logging.info("Endpoint Labels Documentation.")
    wrapper = {}
    response = ResponseDefault()
    allow_ips = AllowedIpAddress()
    ip_address = request.client.host

    category_record = await find_record(
        db=db, table=CategoryDataDocumentation, fetch_type="all"
    )
    object_record = await find_record(
        db=db, table=ObjectDocumentationDetails, fetch_type="all"
    )
    env_record = await find_record(
        db=db, table=EnvironmentDocumentationDetails, fetch_type="all"
    )
    design_type_record = await find_record(
        db=db, table=DesignTypeDocumentationDetails, fetch_type="all"
    )
    time_period_record = await find_record(
        db=db, table=TimePeriodDocumentationDetails, fetch_type="all"
    )
    dominant_color_record = await find_record(
        db=db, table=DominantColorDocumentationDetails, fetch_type="all"
    )
    culture_style_record = await find_record(
        db=db, table=CultureStyleDocumentationDetails, fetch_type="all"
    )

    try:
        if ip_address not in allow_ips.ip_address:
            raise AccessUnauthorized(
                "IP Address blacklisted. Please ask IT Team for add IP as whitelist."
            )

        if category_record:
            for category in category_record:
                if category["category"] == "object":
                    category["details"] = object_record
                if category["category"] == "environment":
                    category["details"] = env_record
                if category["category"] == "design_type":
                    category["details"] = design_type_record
                if category["category"] == "time_period":
                    category["details"] = time_period_record
                if category["category"] == "dominant_colors":
                    category["details"] = dominant_color_record
                if category["category"] == "culture_styles":
                    category["details"] = culture_style_record
            wrapper["documentation"] = category_record
            response.message = "Retrieved all documentation."
            response.data = wrapper
            return response

        response.message = "No documentation found."

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        raise ServiceError(detail=f"Service error: {e}.", name="DiVA")
    return response


router.add_api_route(
    methods=["GET"],
    path="/docs",
    endpoint=labels_documentation,
    summary="Retrieve label documentation.",
    status_code=status.HTTP_200_OK,
)
