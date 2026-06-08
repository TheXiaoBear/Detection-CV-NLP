from ultralytics import YOLO
from cv_app.core.base_model import BaseModel


class YOLOv8Model(BaseModel):

    def __init__(self, weight_path):
        self.weight_path = weight_path
        self.model = None

    def load(self):
        self.model = YOLO(self.weight_path)

    def predict(self, image):
        return self.model(image)

    def unload(self):
        self.model = None