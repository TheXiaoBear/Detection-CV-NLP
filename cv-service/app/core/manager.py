from ultralytics import YOLO

from app.core.config import MODEL_PATH


class ModelManager:

    _model = None

    @classmethod
    def load_model(cls):

        if cls._model is None:

            cls._model = YOLO(str(MODEL_PATH))

        return cls._model

    @classmethod
    def get_model(cls):

        return cls.load_model()