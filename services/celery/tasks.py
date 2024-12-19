import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from services.celery.worker import app
from utils.resnet.execute_model import (
    custom_resnet50_trainer,
    custom_resnet50_fine_tuner,
)
from utils.query.model_card import extract_models_card_entry


@app.task(bind=True)
def train_finetune_custom_resnet50(self) -> None:
    cls_model_available = extract_models_card_entry(model_type="classification")
    if not cls_model_available:
        logging.info("Initialize custom ResNet50.")
        custom_resnet50_trainer()
    custom_resnet50_fine_tuner()
