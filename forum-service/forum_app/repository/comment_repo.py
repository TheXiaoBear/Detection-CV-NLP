from sqlalchemy.orm import Session, aliased

from forum_app.models.comment import Comment
from forum_app.models.user import User


# 创建评论
def create(
        db: Session,
        comment: Comment
):
    db.add(comment)

    return comment


# 查询帖子评论
def get_post_comments(
    db: Session,
    post_id: int
):
    ReplyUser = aliased(User)
    return (
        db.query(
            Comment,
            User.username,
            User.avatar,
            ReplyUser.username
        )
        .outerjoin(
            ReplyUser,
            ReplyUser.id == Comment.reply_user_id
        )
        .join(
            User,
            User.id == Comment.user_id
        )
        .filter(
            Comment.post_id == post_id,
            Comment.deleted_at.is_(None)
        )
        .order_by(Comment.id.desc())
    )


# 根据id查询评论
def get_by_id(
        db: Session,
        comment_id: int
):
    return (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
            Comment.deleted_at.is_(None)
        )
        .first()
    )


# 删除评论
def delete(
        db: Session,
        comment: Comment
):
    db.delete(comment)