from services.celery.worker import app


@app.tasks(bind=True)
def training_custom_resnet50() -> None:
    pass
