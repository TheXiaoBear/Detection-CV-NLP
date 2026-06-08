from sqlalchemy import Column, Integer, String
from cv_app.db.database import Base
from cv_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    role = Column(Integer, default=0)

    description = Column(String(255), nullable=False, default='这个人很懒')

    avatar = Column(String(255), nullable=False, default='https://kakawei.oss-cn-beijing.aliyuncs.com/c78ca35a-54c2-4fff-9117-cdd8e3dd6e17_QQ图片20240618222551.jpg')

    # 一个用户拥有多个任务
    tasks = relationship(
        "Task",
        back_populates="user"
    )