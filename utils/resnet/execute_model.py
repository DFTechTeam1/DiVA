import asyncio
import os
import numpy as np
import torch
from uuid import uuid4
from datetime import datetime
from utils.query.image_tag import extract_validated_image_tag
from utils.helper import label_distribution
from utils.resnet.custom_model import CustomDataLoader, CustomResNet50Classifier
from utils.logger import logging
from petname import generate
from pathlib import Path
from torch.optim import Adam
from torch.utils.data import DataLoader
from torch.nn import BCEWithLogitsLoss
from typing import Literal
from torch import optim
from utils.query.model_card import insert_classification_model_card
from utils.query.model_accuracy import insert_test_accuracy


async def data_loader(dataset: CustomDataLoader) -> CustomDataLoader:
    loop = asyncio.get_event_loop()
    dataloader = await loop.run_in_executor(
        None, lambda: DataLoader(dataset=dataset, shuffle=True)
    )
    return dataloader


async def save_model(model: CustomResNet50Classifier, model_name: str) -> str:
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


async def training_resnet(
    device: Literal["cpu", "gpu"],
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

        logging.info(f"Epoch {epoch+1}, train loss {np.mean(train_loss)}")

    return model


async def validating_resnet(
    device: Literal["cpu", "gpu"],
    dataset: CustomDataLoader,
    dataloader: DataLoader,
    model: CustomResNet50Classifier,
    epochs: int,
) -> None:
    for epoch in range(epochs):
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

        logging.info(f"Epoch {epoch+1}, validation loss {np.mean(val_loss)}")


async def predicting_resnet(
    device: Literal["cpu", "gpu"],
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


async def custom_resnet50_trainer(epochs: int = 100):
    model_name = generate()
    model_path = f"/home/dfactory/Project/DiVA/models/{model_name}.pth"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Start task
    started_task_at = datetime.now()

    # Model unique id
    unique_id = str(uuid4())

    # Data preparation
    entries = await extract_validated_image_tag()
    label_distribution(entries=entries)
    dataset = CustomDataLoader(entries=entries)
    dataset.splitter()
    labels = dataset.label_details()

    # Prepare dataloaders
    dataloader = await data_loader(dataset=dataset)

    # Initialize model
    model = CustomResNet50Classifier(num_labels=labels)
    model = model.to(device=device)
    optimizer = Adam(params=model.parameters(), lr=1e-9)

    # Training, Validation, and Testing (async)
    trained_model = await training_resnet(
        device=device,
        dataloader=dataloader,
        model=model,
        epochs=epochs,
        optimizer=optimizer,
    )
    await validating_resnet(
        device=device,
        dataset=dataset,
        dataloader=dataloader,
        model=trained_model,
        epochs=epochs,
    )
    test_accuracy = await predicting_resnet(
        device=device, dataset=dataset, dataloader=dataloader, model=trained_model
    )

    # Saving model into local project directory
    model_path = await save_model(model=trained_model, model_name=model_name)

    # Finished task
    finished_task_at = datetime.now()

    await insert_classification_model_card(
        started_task_at=started_task_at,
        finished_task_at=finished_task_at,
        unique_id=unique_id,
        model_type="classification",
        model_name=model_name,
        model_path=model_path,
        trained_image=dataset.train_size,
    )

    await insert_test_accuracy(unique_id=unique_id, test_accuracy=test_accuracy)
