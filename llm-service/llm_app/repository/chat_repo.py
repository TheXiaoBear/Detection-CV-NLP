from sqlalchemy.orm import Session

from llm_app.models.chat_messages import (
    ChatMessage
)


class ChatRepository:

    @staticmethod
    def save(
        db: Session,
        report_id: int,
        role: str,
        content: str
    ):

        message = ChatMessage(
            report_id=report_id,
            role=role,
            content=content
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_history(
        db: Session,
        report_id: int
    ):

        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.report_id == report_id
            )
            .order_by(
                ChatMessage.id.asc()
            )
            .all()
        )

    @staticmethod
    def get_recent_history(
            db: Session,
            report_id: int,
            limit: int = 10
    ):
        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.report_id == report_id
            )
            .order_by(
                ChatMessage.id.desc()
            )
            .limit(limit)
            .all()
        )[::-1]

