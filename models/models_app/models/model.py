from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models_app.db.database import Base
from models_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Model(Base, TimestampMixin):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)

    model_name = Column(String(100))

    description = Column(Text)
