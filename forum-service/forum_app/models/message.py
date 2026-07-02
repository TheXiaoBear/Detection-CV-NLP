from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

from datetime import datetime

from forum_app.db.database import Base


class Message(Base):

    __tablename__ = "message"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    # 新增
    post_id = Column(
        Integer,
        nullable=True
    )

    title = Column(
        String(100),
        nullable=False
    )

    content = Column(
        String(500),
        nullable=False
    )

    message_type = Column(
        String(50),
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False
    )

    comment_id = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    target_comment_id = Column(
        Integer,
        nullable=True
    )