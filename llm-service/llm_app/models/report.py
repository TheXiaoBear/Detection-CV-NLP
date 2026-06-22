from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from llm_app.db.database import Base
from llm_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship



class Report(Base, TimestampMixin):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True)

    title = Column(String(50))

    task_id = Column(Integer,  ForeignKey("tasks.id"), unique=True)

    report_type = Column(
        String(50),
        default="cv_report"
    )

    content = Column(Text)

    summary = Column(Text)


