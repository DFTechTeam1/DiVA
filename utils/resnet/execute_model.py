import os
import torch
import numpy as np
from uuid import uuid4
from torch import optim
from pathlib import Path
from typing import Literal
from petname import generate
from datetime import datetime
from torch.optim import Adam
import logging
from torch.nn import BCEWithLogitsLoss
from torch.utils.data import DataLoader
from utils.helper import label_distribution
from utils.query.model_accuracy import insert_test_accuracy
from utils.resnet.custom_model import CustomDataLoader, CustomResNet50Classifier
from utils.query.image_tag import extract_image_tag_entries, update_image_tag_is_trained
from utils.query.model_card import (
    insert_classification_model_card,
    extract_models_card_entry,
    update_model_card_entry,
)


def save_model(model: CustomResNet50Classifier, model_name: str) -> str:
    model_directory = Path("/home/dfactory/Project/DiVA/models")

    if not os.path.exists(path=model_directory):
        logging.info("Creating models directory.")
        os.makedirs(name=model_directory, exist_ok=True)
    else:
        logging.info("Models directory already created.")

    model_path = model_directory / f"{model_name}.pth"
    torch.save(model.state_dict(), model_path)
    logging.info(f"Model {model_name} saved at {model_path}")
    return str(model_path)


def train_validate_resnet(
    device: Literal["cpu", "cuda"],
    dataset: CustomDataLoader,
    dataloader: DataLoader,
    model: CustomResNet50Classifier,
    epochs: int,
    optimizer: optim,
) -> CustomResNet50Classifier:
    for epoch in range(epochs):
        train_loss = []
        model.train()
        for entry in dataloader:
            optimizer.zero_grad()
            image = entry["image"].to(device, dtype=torch.float)
            labels = entry["labels"].to(device, dtype=torch.float)
            y_hat = model(image)
            error = BCEWithLogitsLoss()
            loss = torch.sum(error(y_hat, labels))
            loss.backward()
            optimizer.step()
            train_loss.append(loss.item())

        val_loss = []
        dataset.mode = "valid"
        model.eval()
        with torch.no_grad():
            for data in dataloader:
                image = data["image"].to(device, dtype=torch.float)
                labels = data["labels"].to(device, dtype=torch.float)
                y_hat = model(image)
                error = BCEWithLogitsLoss()
                loss = torch.sum(error(y_hat, labels))
                val_loss.append(loss.item())

        logging.info(
            f"Epoch {epoch+1}\t train loss {np.mean(train_loss):.4}\t validation loss {np.mean(val_loss):.4}"
        )

    return model


def load_resnet(
    num_labels: int, model_path: str, device: Literal["cuda", "gpu"]
) -> CustomResNet50Classifier:
    loaded_model = CustomResNet50Classifier(num_labels=num_labels)
    loaded_model.load_state_dict(torch.load(model_path, weights_only=True))
    loaded_model = loaded_model.to(device)
    return loaded_model.eval()


def predicting_resnet(
    device: Literal["cpu", "cuda"],
    dataset: CustomDataLoader,
    dataloader: DataLoader,
    model: CustomResNet50Classifier,
) -> float:
    dataset.mode = "test"
    model.eval()

    correct_predictions = 0
    total_predictions = 0

    with torch.no_grad():
        for data in dataloader:
            image = data["image"].to(device, dtype=torch.float)
            labels = data["labels"].to(device, dtype=torch.float)
            y_hat = model(image)
            y_prob = torch.sigmoid(y_hat)
            y_pred = (y_prob > 0.5).float()

            correct_predictions += (y_pred == labels).sum().item()
            total_predictions += labels.numel()

    test_accuracy = correct_predictions / total_predictions * 100
    logging.info(f"Test Accuracy: {test_accuracy:.2f}%")
    return float(f"{test_accuracy:.2f}")


def custom_resnet50_trainer(epochs: int = 250) -> None:
    model_name = generate()
    model_path = f"/home/dfactory/Project/DiVA/models/{model_name}.pth"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Start task
    started_task_at = datetime.now()

    # Model unique id
    unique_id = str(uuid4())

    # Data preparation
    entries = extract_image_tag_entries()
    if not entries:
        logging.info("[custom_resnet50_trainer] Skip training.")
    elif len(entries) < 10:
        logging.info(
            "[custom_resnet50_trainer] Skip training. Image threshold not satisfied."
        )
    else:
        label_distribution(entries=entries)
        dataset = CustomDataLoader(entries=entries)
        dataset.splitter()
        labels = dataset.label_details()

        # Prepare dataloaders
        dataloader = DataLoader(dataset=dataset, shuffle=True)

        # Initialize model
        model = CustomResNet50Classifier(num_labels=labels)
        model = model.to(device=device)
        optimizer = Adam(params=model.parameters(), lr=1e-5)

        # Training, Validation, and Testing (async)
        trained_model = train_validate_resnet(
            dataset=dataset,
            device=device,
            dataloader=dataloader,
            model=model,
            epochs=epochs,
            optimizer=optimizer,
        )

        test_accuracy = predicting_resnet(
            device=device, dataset=dataset, dataloader=dataloader, model=trained_model
        )

        # Saving model into local project directory
        model_path = save_model(model=trained_model, model_name=model_name)

        # Finished task
        finished_task_at = datetime.now()

        insert_classification_model_card(
            started_task_at=started_task_at,
            finished_task_at=finished_task_at,
            unique_id=unique_id,
            model_type="classification",
            model_name=model_name,
            model_path=model_path,
            trained_image=dataset.train_size,
        )

        insert_test_accuracy(unique_id=unique_id, test_accuracy=test_accuracy)
        update_image_tag_is_trained(entries=entries)


def custom_resnet50_fine_tuner(epochs: int = 250) -> None:
    cls_model = extract_models_card_entry(model_type="classification")
    entries = extract_image_tag_entries()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if not entries:
        logging.info("[custom_resnet50_fine_tuner] No updated validated data.")
    elif len(entries) < 10:
        logging.info(
            "[custom_resnet50_fine_tuner] Skip fine tuning. Image threshold not satisfied."
        )
    else:
        logging.info(
            f"[custom_resnet50_fine_tuner] Found new {len(entries)} images. Proceed fine tuning phase."
        )
        # Start task
        started_task_at = datetime.now()

        # Data preparation
        label_distribution(entries=entries)
        dataset = CustomDataLoader(entries=entries)
        dataset.splitter()
        labels = dataset.label_details()
        trained_image = dataset.train_size + cls_model.trained_image

        # Prepare dataloaders
        dataloader = DataLoader(dataset=dataset, shuffle=True)

        # Load resnet model
        model = load_resnet(
            num_labels=labels, model_path=cls_model.model_path, device=device
        )
        optimizer = Adam(params=model.parameters(), lr=1e-5)

        # Training, Validation, and Testing (async)
        trained_model = train_validate_resnet(
            dataset=dataset,
            device=device,
            dataloader=dataloader,
            model=model,
            epochs=epochs,
            optimizer=optimizer,
        )

        test_accuracy = predicting_resnet(
            device=device, dataset=dataset, dataloader=dataloader, model=trained_model
        )

        # Updating model into local project directory
        save_model(model=trained_model, model_name=cls_model.model_name)

        # Finished task
        finished_task_at = datetime.now()

        logging.info("[custom_resnet50_fine_tuner] Updating model card.")
        update_model_card_entry(
            started_task_at=started_task_at,
            finished_task_at=finished_task_at,
            model_type="classification",
            trained_image=trained_image,
        )

        insert_test_accuracy(unique_id=cls_model.unique_id, test_accuracy=test_accuracy)
        update_image_tag_is_trained(entries=entries)
    return None
