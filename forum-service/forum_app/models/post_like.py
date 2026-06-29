from sqlalchemy import (
    Column,
    Integer,
    UniqueConstraint
)

from forum_app.db.database import Base
from forum_app.models.mixins import TimestampMixin


class PostLike(Base, TimestampMixin):
    __tablename__ = "post_likes"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_user_post_like"
        ),
    )

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

    post_id = Column(
        Integer,
        nullable=False,
        index=True
    )