from ultralytics import YOLO

from cv_app.core.config import MODEL_PATHS


class ModelManager:

    _models = {}

    _current_model = None

    @classmethod
    def load_model(cls, model_name: str):

        if model_name not in MODEL_PATHS:
            raise Exception(f"模型 {model_name} 不存在")

        if model_name not in cls._models:

            model_path = MODEL_PATHS[model_name]

            cls._models[model_name] = YOLO(str(model_path))

        cls._current_model = model_name

        return cls._models[model_name]

    @classmethod
    def switch_model(cls, model_name: str):

        return cls.load_model(model_name)

    @classmethod
    def get_model(cls):

        if cls._current_model is None:

            cls.load_model("yolov8n")

        return cls._models[cls._current_model]

    @classmethod
    def get_current_model_name(cls):

        return cls._current_model

    @classmethod
    def get_loaded_models(cls):

        return list(cls._models.keys())

    @classmethod
    def get_available_models(cls):

        return list(MODEL_PATHS.keys())