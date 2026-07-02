# models/post_favorite.py

from sqlalchemy import (
    Column,
    Integer
)

from forum_app.db.database import Base
from forum_app.models.mixins import TimestampMixin


class PostFavorite(
    Base,
    TimestampMixin
):
    __tablename__ = "post_favorites"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    post_id = Column(
        Integer,
        nullable=False,
        index=True
    )