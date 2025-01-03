from contextlib import asynccontextmanager
from src.secret import Config
from fastapi import FastAPI, status
from src.routers import health_check
from fastapi.middleware.cors import CORSMiddleware
from services.postgres.models import database_migration
from services.postgres.connection import database_connection
from starlette.middleware.sessions import SessionMiddleware
from utils.query.labels_documentation import initialize_labels_documentation
from utils.query.image_tag import initialize_image_tag_preparation
from src.routers.enrich_knowledge import train_models
from src.routers.monitor_task import monitor_task
from src.routers.classification import pagination, labels_validator, documentation
from src.routers.nas_directory_manager import (
    create_directory,
    delete_directory,
    move_directory,
    update_directory,
)
from utils.custom_errors import (
    DiVA,
    DataNotFoundError,
    ServicesConnectionError,
    DatabaseQueryError,
    NasIntegrationError,
    AccessUnauthorized,
    create_exception_handler,
)


config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database_migration()
        await database_migration()
        await initialize_labels_documentation()
        await initialize_image_tag_preparation()
        yield
    finally:
        await database_connection(connection_type="async").dispose()


app = FastAPI(
    root_path="/api/v1",
    title="DiVA",
    description="Backend service for DFactory Image Retrieval.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    middleware_class=SessionMiddleware, secret_key=config.MIDDLEWARE_SECRET_KEY
)

app.include_router(health_check.router)
app.include_router(create_directory.router)
app.include_router(update_directory.router)
app.include_router(delete_directory.router)
app.include_router(move_directory.router)
app.include_router(documentation.router)
app.include_router(pagination.router)
app.include_router(labels_validator.router)
app.include_router(train_models.router)
app.include_router(monitor_task.router)

app.add_exception_handler(
    exc_class_or_status_code=DiVA,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail_message="A service seems to be down, try again later.",
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=DataNotFoundError,
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
