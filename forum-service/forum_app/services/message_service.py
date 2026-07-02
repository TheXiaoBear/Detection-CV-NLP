from sqlalchemy.orm import Session

from forum_app.models.message import Message

from forum_app.repository import (
    message_repo
)

def create_message(
        db: Session,
        user_id: int,
        title: str,
        content: str,
        message_type: str,
        post_id: int = None,
        comment_id=None,
        target_comment_id: int = None
):
    message = Message(
        user_id=user_id,
        post_id=post_id,
        target_comment_id=target_comment_id,
        comment_id=comment_id,
        title=title,
        content=content,
        message_type=message_type
    )

    message_repo.create(
        db,
        message
    )

    return message


def my_messages(
        db: Session,
        user_id: int,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = message_repo.get_by_user(
        db,
        user_id
    )

    total = query.count()

    records = (
        query
        .order_by(
            Message.id.desc()
        )
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return {
        "records": records,
        "totalRow": total
    }

def read_message(
        db: Session,
        user_id: int,
        message_id: int
):

    message = (
        message_repo.get_by_id(
            db,
            message_id
        )
    )

    if not message:
        return False

    if message.user_id != user_id:
        return False

    message.is_read = True

    db.commit()

    return True

def unread_count(
        db: Session,
        user_id: int
):

    return {
        "count":
        message_repo.get_unread_count(
            db,
            user_id
        )
    }

def read_all_messages(
        db: Session,
        user_id: int
):

    message_repo.read_all(
        db,
        user_id
    )

    db.commit()

    return True