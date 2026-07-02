from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_app.models.post import Post

from forum_app.repository import post_repo

from forum_app.schemas.post import (
    PostCreate,
    PostUpdate
)
from forum_app.repository import (
    like_repo,
    favorite_repo
)


def create_post(
        db: Session,
        user_id: int,
        post_in: PostCreate
):

    post = Post(
        user_id=user_id,
        title=post_in.title,
        content=post_in.content
    )

    post_repo.create(
        db,
        post
    )

    db.commit()

    db.refresh(post)

    return post

def get_post(
        db: Session,
        post_id: int,
        user_id=None
):
    row = post_repo.get_new_detail(
        db,
        post_id
    )

    liked = False
    favorited = False

    if user_id:
        liked = like_repo.is_liked(
            db,
            user_id,
            post_id
        )

        favorited = favorite_repo.is_favorited(
            db,
            user_id,
            post_id
        )

    if not row:
        raise HTTPException(
            404,
            "帖子不存在"
        )

    post, username, avatar = row

    if not post:
        raise HTTPException(
            404,
            "帖子不存在"
        )

    post.view_count += 1

    db.commit()

    db.refresh(post)

    return {

        "id": post.id,

        "title": post.title,

        "content": post.content,

        "user_id": post.user_id,

        "view_count": post.view_count,

        "like_count": post.like_count,

        "comment_count": post.comment_count,

        "created_at": post.created_at,

        "liked": liked,

        "favorited": favorited,

        "author": {

            "id": post.user_id,

            "username": username,

            "avatar": avatar

        }

    }

def update_post(
        db: Session,
        user_id: int,
        post_id: int,
        post_in: PostUpdate
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

    if post.user_id != user_id:
        raise HTTPException(
            403,
            "无权限修改"
        )

    for k, v in (
        post_in.model_dump(
            exclude_unset=True
        ).items()
    ):
        setattr(post, k, v)

    db.commit()

    db.refresh(post)

    return post

def delete_post(
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

    if post.user_id != user_id:
        raise HTTPException(
            403,
            "无权限删除"
        )

    post_repo.delete(
        db,
        post
    )

    db.commit()

    return True

def get_posts(
        db: Session,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = post_repo.get_all(db)

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

            "comment_count": post.comment_count,

            "created_at": post.created_at,

            "username": username,

            "avatar": avatar

        })

    return {
        "records": records,
        "totalRow": total
    }

def search_post(
        db: Session,
        keyword: str,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = post_repo.search(
        db,
        keyword
    )

    total = query.count()

    rows = (
        query
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

            "comment_count": post.comment_count,

            "created_at": post.created_at,

            "username": username,

            "avatar": avatar

        })

    return {
        "records": records,
        "totalRow": total
    }

def my_posts(
        db: Session,
        user_id: int,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = post_repo.get_by_user_id(
        db,
        user_id
    )

    total = query.count()

    rows = (
        query
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

            "comment_count": post.comment_count,

            "created_at": post.created_at,

            "username": username,

            "avatar": avatar

        })

    return {
        "records": records,
        "totalRow": total
    }