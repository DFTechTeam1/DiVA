# TODO: add enrich knowledge train model capabilities if model already created else create new model

import os
import pandas as pd
import numpy as np
import torch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.logger import logging
from petname import generate
from pathlib import Path
from torch.optim import Adam
from utils.resnet import MultiLabelDataset, MultiLabelClassifier
from torch.utils.data import DataLoader
from torch.nn import BCEWithLogitsLoss

csv_path = Path("/project_utils/diva/backup_db/backup_image_tag.csv")
df = pd.read_csv(filepath_or_buffer=csv_path, delimiter=",")

for column in df.iloc[:, 5:-2].columns:
    df[column] = pd.to_numeric(df[column]).astype(int)
    value_counts = df[column].value_counts(normalize=True) * 100
    logging.info(f"Label percentages: {value_counts.to_string()}")

dataset = MultiLabelDataset(dataset_path=csv_path)
dataset.splitter()
device = "cuda" if torch.cuda.is_available() else "cpu"
dataloader = DataLoader(dataset=dataset, shuffle=True)
labels = dataset.show_total_label()
model = MultiLabelClassifier(num_labels=labels)
model = model.to(device=device)
learning_rate = 1e-9
epochs = 100
optimizer = Adam(params=model.parameters(), lr=learning_rate)
model_dir = Path("/home/dfactory/Project/DiVA/models")


def validate_model_availability() -> str | None:
    is_model_available = os.listdir(path=model_dir)[0]
    if is_model_available:
        logging.info(f"Model {is_model_available[-1]} already created.")
        return is_model_available[-1]
    logging.warning(
        "Model is not available. Perform first custom ResNet50 training phase."
    )
    return None


def load_model():
    model = validate_model_availability()
    if model:
        pass


def train_custom_resnet50(epochs: int) -> MultiLabelClassifier:
    epoch_train_loss = []
    epoch_val_loss = []

    for epoch in range(epochs):
        train_loss = []
        dataset.mode = "train"
        model.train()
        for data in dataloader:
            optimizer.zero_grad()
            image = data["image"].to(device, dtype=torch.float)
            labels = data["labels"].to(device, dtype=torch.float)
            y_hat = model(image)
            error = BCEWithLogitsLoss()
            loss = torch.sum(error(y_hat, labels))
            loss.backward()
            optimizer.step()
            train_loss.append(loss.item())
        epoch_train_loss.append(np.mean(train_loss))

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
        epoch_val_loss.append(np.mean(train_loss))

        logging.info(
            f"Epoch {epoch+1} \t train loss {np.mean(train_loss)} \t val loss {np.mean(val_loss)}"
        )

    if not os.path.exists(path=model_dir):
        logging.info("Creating models directory.")
        os.makedirs(name=model_dir, exist_ok=True)
    else:
        logging.info("Models directory already created.")

    model_name = generate()
    model_path = model_dir / f"{model_name}.pth"
    torch.save(model.state_dict(), model_path)
    logging.info(f"Model {model_name} saved at {model_path}.")

    return model


model = train_custom_resnet50(epochs=2)
