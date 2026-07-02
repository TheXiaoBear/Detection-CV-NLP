from sqlalchemy.orm import Session
from forum_app.models.user import User

def get_by_id(
        db: Session,
        user_id: int
):

    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )