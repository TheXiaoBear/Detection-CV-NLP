from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_app.models.post_like import PostLike

from forum_app.repository import (
    like_repo,
    post_repo,
    user_repo
)
from forum_app.services import (
    message_service
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

    if post.user_id != user_id:
        current_user = (
            user_repo.get_by_id(
                db,
                user_id
            )
        )

        message_service.create_message(
            db,
            post.user_id,
            "帖子收到点赞",
            f"{current_user.username} 点赞了你的帖子《{post.title}》",
            "like",
            post.id
        )

    db.commit()

    return {
        "liked": True
    }