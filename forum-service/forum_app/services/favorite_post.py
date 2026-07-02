from sqlalchemy.orm import Session
from fastapi import HTTPException
from forum_app.models.post import Post
from forum_app.models.post_favorite import PostFavorite

from forum_app.repository import (
    favorite_repo,
    post_repo,
    user_repo
)

from forum_app.services import (
    message_service
)


def toggle_favorite(
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

    favorite = favorite_repo.get_favorite(
        db,
        user_id,
        post_id
    )

    # 已收藏
    if favorite:

        favorite_repo.delete(
            db,
            favorite
        )

        if post.favorite_count > 0:
            post.favorite_count -= 1

        db.commit()

        return {
            "favorited": False
        }

    # 未收藏
    favorite = PostFavorite(
        user_id=user_id,
        post_id=post_id
    )

    favorite_repo.create(
        db,
        favorite
    )

    if post.favorite_count is None:
        post.favorite_count = 0

    post.favorite_count += 1

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
            "帖子被收藏",
            f"{current_user.username} 收藏了你的帖子《{post.title}》",
            "favorite",
            post.id
        )

    db.commit()

    return {
        "favorited": True
    }

def my_favorites(
        db: Session,
        user_id: int,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = favorite_repo.get_favorite_posts(
        db,
        user_id
    )

    total = query.count()

    rows = (
        query
        .order_by(Post.id.desc())
        .offset(skip)
        .limit(page_size)
        .all()
    )

    records = []

    for post, username, avatar in rows:
        records.append({

            "id": post.id,

            "title": post.title,

            "content": post.content,

            "user_id": post.user_id,

            "view_count": post.view_count,

            "like_count": post.like_count,

            "favorite_count": post.favorite_count,

            "comment_count": post.comment_count,

            "created_at": post.created_at,

            "username": username,

            "avatar": avatar

        })

    return {
        "records": records,
        "totalRow": total
    }