from sqlalchemy import Column, Integer, String, ForeignKey
from models_app.db.database import Base
from models_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship(
        "Task",
        back_populates="favorites"
    )

    user = relationship("User", back_populates="favorites")