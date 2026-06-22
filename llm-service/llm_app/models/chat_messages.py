from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from llm_app.db.database import Base
from llm_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship

class ChatMessage(
    Base,
    TimestampMixin
):
    __tablename__ = "chat_messages"

    id = Column(
        Integer,
        primary_key=True
    )

    report_id = Column(
        Integer,
        ForeignKey("report.id")
    )

    role = Column(
        String(20)
    )

    content = Column(
        Text
    )