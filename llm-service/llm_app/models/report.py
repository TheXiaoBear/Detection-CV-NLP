from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from llm_app.db.database import Base
from llm_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship



class Report(Base, TimestampMixin):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer)

    report_type = Column(String(50))

    content = Column(Text)


