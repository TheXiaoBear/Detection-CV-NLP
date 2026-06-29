from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_app.models.post_like import PostLike

from forum_app.repository import (
    like_repo,
    post_repo
)


def toggle_like(
        db: Session,
        user_id: int,
        post_id: int
):

    post = post_repo.get_by_id(
        db,
        post_id
    )

    if not post:
        raise HTTPException(
            404,
            "帖子不存在"
        )

    like = like_repo.get_like(
        db,
        user_id,
        post_id
    )

    # 已点赞
    if like:

        like_repo.delete(
            db,
            like
        )

        if post.like_count > 0:
            post.like_count -= 1

        db.commit()

        return {
            "liked": False
        }

    # 未点赞
    like = PostLike(
        user_id=user_id,
        post_id=post_id
    )

    like_repo.create(
        db,
        like
    )

    post.like_count += 1

    db.commit()

    return {
        "liked": True
    }