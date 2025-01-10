import cv2
import numpy as np
from PIL import Image
from tqdm.auto import tqdm
from typing import Literal
from sklearn.model_selection import train_test_split
from torchvision.models import ResNet50_Weights
from torchvision import models
from torch.nn import Module, Linear


class CustomDataLoader:
    def __init__(self, entries: list[dict]) -> None:
        self.images = []
        self.labels = []
        self.x_train = None
        self.x_val = None
        self.x_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.train_size = None
        self.val_size = None
        self.test_size = None
        self.mode: Literal["train", "valid", "test"] = "train"

        for record in tqdm(iterable=entries, desc="Loading entries."):
            filepath = record["filepath"]
            label_values = list(record.values())[5:-2]

            self.labels.append(label_values)

            img = Image.open(filepath).convert("RGB")
            array = np.array(img)
            resized_image = cv2.resize(array, (224, 224))
            image = resized_image.reshape((3, 224, 224))
            self.images.append(image)

        self.images = np.array(self.images) / 255
        self.labels = np.array(self.labels)

    def splitter(self) -> None:
        """
        The function `splitter` splits the images and labels data into training, testing, and validation
        sets using the `train_test_split` function.

        :param test_size: The `test_size` parameter in the `splitter` method represents the proportion
        of the dataset to include in the test split. It is a float value between 0.0 and 1.0 and
        represents the fraction of the dataset to be included in the test split. For example, if
        :type test_size: int
        """
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.images, self.labels, test_size=0.1)
        self.x_train, self.x_val, self.y_train, self.y_val = train_test_split(self.x_train, self.y_train, test_size=0.1)

        self.train_size = self.x_train.shape[0]
        self.val_size = self.x_val.shape[0]
        self.test_size = self.x_test.shape[0]

    def label_details(self) -> int:
        """
        This function returns the length of the first element in the 'labels' attribute of the object.
        :return: The `label_details` method is returning the length of the first element in the `labels`
        list of the object instance.
        """
        return len(self.labels[0])

    def __len__(self) -> int:
        """
        This function returns the length of the data based on the mode specified (test, valid, or
        train).
        :return: The `__len__` method is returning the number of samples in the dataset based on the
        mode specified. If the mode is "test", it returns the number of samples in the x_test data. If
        the mode is "valid", it returns the number of samples in the x_val data. Otherwise, it returns
        the number of samples in the x_train data.
        """
        if self.mode == "test":
            return self.x_test.shape[0]
        if self.mode == "valid":
            return self.x_val.shape[0]
        return self.x_train.shape[0]

    def __getitem__(self, index) -> dict:
        """
        This function returns a dictionary containing image and label data based on the mode specified.

        :param index: The `index` parameter in the `__getitem__` method refers to the index of the item you
        want to retrieve from the dataset. It is used to access a specific data point within the dataset
        based on the index provided
        :return: The `__getitem__` method is returning a dictionary with keys "image" and "labels"
        containing the corresponding data based on the mode specified ("test", "valid", or default).
        """
        if self.mode == "test":
            return {"image": self.x_test[index], "labels": self.y_test[index]}
        if self.mode == "valid":
            return {"image": self.x_val[index], "labels": self.y_val[index]}
        return {"image": self.x_train[index], "labels": self.y_train[index]}


class CustomResNet50Classifier(Module):
    def __init__(self, num_labels: int) -> None:
        super(CustomResNet50Classifier, self).__init__()
        self.custom_resnet50_model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.in_features = self.custom_resnet50_model.fc.in_features
        self.custom_resnet50_model.fc = Linear(in_features=self.in_features, out_features=num_labels)

    def forward(self, image):
        return self.custom_resnet50_model(image)
