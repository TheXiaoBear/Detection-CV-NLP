from sqlalchemy.orm import Session

from forum_app.models.message import Message


def create(
        db: Session,
        message: Message
):
    db.add(message)

    return message


def get_by_user(
        db: Session,
        user_id: int
):

    return (
        db.query(Message)
        .filter(
            Message.user_id == user_id
        )
    )


def get_by_id(
        db: Session,
        message_id: int
):

    return (
        db.query(Message)
        .filter(
            Message.id == message_id
        )
        .first()
    )

def get_unread_count(
        db: Session,
        user_id: int
):

    return (
        db.query(Message)
        .filter(
            Message.user_id == user_id,
            Message.is_read == False
        )
        .count()
    )

def read_all(
        db: Session,
        user_id: int
):

    return (
        db.query(Message)
        .filter(
            Message.user_id == user_id,
            Message.is_read == False
        )
        .update(
            {
                "is_read": True
            }
        )
    )
