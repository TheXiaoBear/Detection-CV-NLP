from sqlalchemy.orm import Session

from forum_app.models.comment import Comment


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
    return (
        db.query(Comment)
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