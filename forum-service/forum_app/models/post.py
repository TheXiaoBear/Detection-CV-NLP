from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from forum_app.db.database import Base
from forum_app.models.mixins import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    favorite_count = Column(
        Integer,
        nullable=False,
        default=0
    )

    view_count = Column(
        Integer,
        default=0
    )

    like_count = Column(
        Integer,
        default=0
    )

    comment_count = Column(
        Integer,
        default=0
    )