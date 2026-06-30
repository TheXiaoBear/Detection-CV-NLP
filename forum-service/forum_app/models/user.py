from sqlalchemy import (
    Column,
    Integer,
    String
)

from forum_app.db.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String(50)
    )

    avatar = Column(
        String(255)
    )