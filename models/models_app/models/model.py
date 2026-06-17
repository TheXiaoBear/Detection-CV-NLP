from sqlalchemy import Column, Integer, String, ForeignKey
from favorite_app.db.database import Base
from favorite_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Model(Base, TimestampMixin):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)

    model_name = Column(String)

    description = Column(String)
