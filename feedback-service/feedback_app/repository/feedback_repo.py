from sqlalchemy.orm import Session

from feedback_app.models.feedback import Feedback
from feedback_app.models.user import User
# 创建
def create(
        db: Session,
        feedback: Feedback
):
    db.add(feedback)

    return feedback

# 查询我的反馈
def get_by_user(
        db: Session,
        user_id: int
):

    return (
        db.query(Feedback)
        .filter(
            Feedback.user_id == user_id,
            Feedback.deleted_at.is_(None)
        )
    )

# 查询全部
def get_all(
        db: Session
):

    return (
        db.query(
            Feedback,
            User.username
        )
        .join(
            User,
            User.id == Feedback.user_id
        )
        .filter(
            Feedback.deleted_at.is_(None)
        )
    )

# 根据ID
def get_by_id(
        db: Session,
        feedback_id: int
):
    return (
        db.query(Feedback)
        .filter(
            Feedback.id == feedback_id,
            Feedback.deleted_at.is_(None)
        )
        .first()
    )