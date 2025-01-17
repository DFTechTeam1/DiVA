import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, status
from utils.custom_error import ServiceError, DataNotFoundError, DiVA

router = APIRouter(tags=["Images"], prefix="/images")


async def get_image(relative_path: str):
    file_path = Path(f"./static/{relative_path}")

    try:
        if not Path("./static").exists():
            raise DataNotFoundError(detail="Static directory not found.")

        if not file_path.exists():
            raise DataNotFoundError(detail="Image not found.")

        with file_path.open("rb") as image_file:
            buf = io.BytesIO(image_file.read())
            buf.seek(0)
            ext = relative_path.split(".")[-1]

            response = StreamingResponse(
                content=buf,
                media_type=f"image/{ext}",
                headers={"Content-Disposition": f'inline; filename="{file_path.name}"'},
            )
    except DiVA:
        raise
    except Exception as e:
        raise ServiceError(detail=f"Error reading the image: {str(e)}", name="DiVA")

    return response


router.add_api_route(
    methods=["GET"],
    path="/{relative_path:path}",
    endpoint=get_image,
    summary="Retrieve chunked image entries.",
    status_code=status.HTTP_200_OK,
)
