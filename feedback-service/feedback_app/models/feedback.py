from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from feedback_app.db.database import Base
from feedback_app.models.mixins import TimestampMixin


class Feedback(Base, TimestampMixin):

    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    title = Column(
        String(100),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    feedback_type = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(20),
        default="pending"
    )

    admin_reply = Column(
        Text,
        nullable=True
    )