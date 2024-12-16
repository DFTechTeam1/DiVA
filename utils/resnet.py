import cv2
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from PIL import Image
from torch.utils.data import ConcatDataset
from sklearn.model_selection import train_test_split
from torchvision.models import ResNet50_Weights
from torchvision import models
from typing import Literal
from torch.nn import Module, Linear


class Dataset(object):
    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __add__(self, other):
        return ConcatDataset([self, other])


class MultiLabelDataset(Dataset):
    def __init__(self, dataset_path: str) -> None:
        self.labels = []
        self.images = []
        self.x_train = None
        self.x_val = None
        self.x_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.mode: Literal["train", "valid", "test"] = "train"

        df = pd.read_csv(filepath_or_buffer=dataset_path, delimiter=",")
        df = df.iloc[:30]
        labels = df.iloc[:, 5:-2].values

        self.labels = labels

        for path in tqdm(df["filepath"]):
            img = Image.open(path).convert("RGB")
            array = np.array(img)
            resized_image = cv2.resize(array, (224, 224))
            image = resized_image.reshape((3, 224, 224))
            self.images.append(image)

        self.images = np.array(self.images)
        self.normalize()

    def splitter(self) -> None:
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.images, self.labels, test_size=0.3
        )
        self.x_train, self.x_val, self.y_train, self.y_val = train_test_split(
            self.x_train, self.y_train, test_size=0.3
        )

    def normalize(self) -> None:
        self.images = self.images / 255

    def show_total_label(self) -> int:
        return len(self.labels[0])

    def __len__(self) -> int:
        if self.mode == "test":
            return self.x_test.shape[0]
        if self.mode == "valid":
            return self.x_val.shape[0]
        return self.x_train.shape[0]

    def __getitem__(self, index) -> dict:
        if self.mode == "test":
            return {"image": self.x_test[index], "labels": self.x_test[index]}
        if self.mode == "valid":
            return {"image": self.x_val[index], "labels": self.y_val[index]}
        return {"image": self.x_train[index], "labels": self.y_train[index]}


class MultiLabelClassifier(Module):
    def __init__(self, num_labels: int) -> None:
        super(MultiLabelClassifier, self).__init__()
        self.custom_resnet50_model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.in_features = self.custom_resnet50_model.fc.in_features
        self.custom_resnet50_model.fc = Linear(
            in_features=self.in_features, out_features=num_labels
        )

    def forward(self, image):
        return self.custom_resnet50_model(image)
