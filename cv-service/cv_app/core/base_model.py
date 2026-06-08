from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self, image):
        pass

    @abstractmethod
    def unload(self):
        pass