from celery import Celery
from src.secret import Config

config = Config()

app = Celery(
    main="diva_bg_task",
    backend=config.PGSQL_BACKEND,
    broker=config.BROKER_URL,
)

app.autodiscover_tasks(["services.celery.tasks"])
