from sqlalchemy import Column, Integer, String, ForeignKey, Text
from notice_app.db.database import Base
from notice_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Notice(Base, TimestampMixin):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    user_name = Column(String(50))  #  加上长度
    title = Column(String(100))  #  加上长度
    content = Column(Text)  #  公告内容较长，建议用 Text 替代 String