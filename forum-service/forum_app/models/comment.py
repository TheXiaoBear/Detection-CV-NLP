from sqlalchemy import (
    Column,
    Integer,
    Text
)

from forum_app.db.database import Base
from forum_app.models.mixins import TimestampMixin


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    post_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )