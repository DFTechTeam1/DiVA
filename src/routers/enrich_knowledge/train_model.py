from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault

router = APIRouter(tags=["Enrich Knowledge"])


async def train_resnet_and_clip_encoding() -> ResponseDefault:
    response = ResponseDefault()
    logging.info("Endpoint Enrich Knowledge.")
    return response


router.add_api_route(
    methods=["POST"],
    path="/train-models",
    endpoint=train_resnet_and_clip_encoding,
    summary="Enrich knowledge custom ResNet50 and clip-ViT-B-32.",
    status_code=status.HTTP_200_OK,
)
