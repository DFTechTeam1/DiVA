from services.celery.worker import app


@app.tasks(bind=True)
def training_custom_resnet50() -> None:
    pass
    # cls_model_available = await extract_models_card_entry(model_type='classification')
    # if not cls_model_available:
    #     logging.info(f"Initialize custom ResNet50.")
    #     return await custom_resnet50_trainer()
    # return await custom_resnet50_fine_tuner()
