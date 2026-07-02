from sqlalchemy.orm import Session
from fastapi import HTTPException

from feedback_app.models.feedback import Feedback

from feedback_app.repository import (
    feedback_repo
)

from feedback_app.schemas.feedback import (
    FeedbackCreate,
    FeedbackReply
)


def create_feedback(
        db: Session,
        user_id: int,
        feedback_in: FeedbackCreate
):

    feedback = Feedback(
        user_id=user_id,
        title=feedback_in.title,
        content=feedback_in.content,
        feedback_type=feedback_in.feedback_type
    )

    feedback_repo.create(
        db,
        feedback
    )

    db.commit()

    db.refresh(feedback)

    return feedback


def my_feedback(
        db: Session,
        user_id: int,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = (
        feedback_repo.get_by_user(
            db,
            user_id
        )
    )

    total = query.count()

    rows = (
        query
        .order_by(
            Feedback.id.desc()
        )
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return {
        "records": rows,
        "totalRow": total
    }


def get_feedback_detail(
        db: Session,
        feedback_id: int,
        user_id: int,
):

    feedback = (
        feedback_repo.get_by_id(
            db,
            feedback_id
        )
    )

    if not feedback:
        raise HTTPException(
            404,
            "反馈不存在"
        )

    if feedback.user_id != user_id:
        raise HTTPException(
            403,
            "无权限查看"
        )

    return feedback


def admin_feedback_detail(
        db: Session,
        feedback_id: int
):

    feedback = (
        feedback_repo.get_by_id(
            db,
            feedback_id
        )
    )

    if not feedback:
        raise HTTPException(
            404,
            "反馈不存在"
        )

    return feedback

def get_feedback_list(
        db: Session,
        page_num: int,
        page_size: int,
        status: str = None
):

    skip = (
        page_num - 1
    ) * page_size

    query = (
        feedback_repo.get_all(db)
    )
    if status:
        query = query.filter(
            Feedback.status == status
        )

    total = query.count()

    rows = (
        query
        .order_by(
            Feedback.id.desc()
        )
        .offset(skip)
        .limit(page_size)
        .all()
    )

    records = []

    for feedback, username in rows:
        records.append({

            "id": feedback.id,

            "user_id": feedback.user_id,

            "username": username,

            "title": feedback.title,

            "content": feedback.content,

            "feedback_type": feedback.feedback_type,

            "status": feedback.status,

            "admin_reply": feedback.admin_reply,

            "created_at": feedback.created_at

        })

    return {

        "records": records,

        "totalRow": total

    }


def reply_feedback(
        db: Session,
        feedback_id: int,
        reply_in: FeedbackReply
):

    feedback = (
        feedback_repo.get_by_id(
            db,
            feedback_id
        )
    )

    if not feedback:
        raise HTTPException(
            404,
            "反馈不存在"
        )

    feedback.admin_reply = (
        reply_in.admin_reply
    )

    feedback.status = "resolved"

    db.commit()

    db.refresh(feedback)

    return feedback