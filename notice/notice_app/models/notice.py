from sqlalchemy import Column, Integer, String, ForeignKey
from notice_app.db.database import Base
from notice_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Notice(Base, TimestampMixin):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    user_name = Column(String)

    title = Column(String)

    content = Column(String)