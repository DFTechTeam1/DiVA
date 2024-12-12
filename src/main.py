from src.secret import Config
from fastapi import FastAPI, status
from src.routers import health_check
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from utils.custom_errors import (
    DiVA,
    NotFoundError,
    ServicesConnectionError,
    DatabaseQueryError,
    NasIntegrationError,
    AccessUnauthorized,
    create_exception_handler,
)

config = Config()

app = FastAPI(
    root_path="/api/v1",
    title="Image Search Engine",
    description="Backend service for Image Search Engine project.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    middleware_class=SessionMiddleware,
    secret_key=config.MIDDLEWARE_SECRET_KEY,
)

app.include_router(health_check.router)

app.add_exception_handler(
    exc_class_or_status_code=DiVA,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail_message="A service seems to be down, try again later.",
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=NotFoundError,
    handler=create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail_message="File or data not found.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=ServicesConnectionError,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_message="Service currently not available.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=DatabaseQueryError,
    handler=create_exception_handler(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_message="Invalid database query.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=NasIntegrationError,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_message="Request into NAS not eligible.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=AccessUnauthorized,
    handler=create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        detail_message="Blacklist certain IP address to access the service.",
    ),
)
