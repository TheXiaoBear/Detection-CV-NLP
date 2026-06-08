from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from user_app.db.database import Base
from user_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Result(Base, TimestampMixin):

    __tablename__ = "results"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.id"))

    label = Column(String(100))

    confidence = Column(Float)

    sentence = Column(Text)

    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)

    task = relationship(
        "Task",
        back_populates="results"
    )