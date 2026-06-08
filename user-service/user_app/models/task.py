from sqlalchemy import Column, Integer, String, ForeignKey, Text
from user_app.db.database import Base
from user_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    # 多对一 -> user
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    title = Column(String(50))

    image_path = Column(String(255))

    description = Column(Text)

    status = Column(String(50), index=True, nullable=False)

    bbox_image = Column(String(500))

    heatmap_image = Column(String(500))

    cv_model = Column(String(50))
    nlp_model = Column(String(50))

    user = relationship("User",
                        back_populates="tasks")

    # 一对多 -> result
    results = relationship("Result",
                           back_populates="task")