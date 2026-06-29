from sqlalchemy.orm import Session

from forum_app.models.post_like import PostLike


# 查询点赞
def get_like(
        db: Session,
        user_id: int,
        post_id: int
):
    return (
        db.query(PostLike)
        .filter(
            PostLike.user_id == user_id,
            PostLike.post_id == post_id
        )
        .first()
    )


# 创建点赞
def create(
        db: Session,
        like: PostLike
):
    db.add(like)

    return like


# 删除点赞
def delete(
        db: Session,
        like: PostLike
):
    db.delete(like)