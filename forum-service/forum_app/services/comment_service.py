from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_app.models.comment import Comment

from forum_app.repository import (
    comment_repo,
    post_repo
)

from forum_app.schemas.comment import (
    CommentCreate
)


def create_comment(
        db: Session,
        user_id: int,
        comment_in: CommentCreate
):

    post = post_repo.get_by_id(
        db,
        comment_in.post_id
    )

    if not post:
        raise HTTPException(
            404,
            "帖子不存在"
        )

    comment = Comment(
        post_id=comment_in.post_id,
        user_id=user_id,
        content=comment_in.content
    )

    comment_repo.create(
        db,
        comment
    )

    post.comment_count += 1

    db.commit()

    db.refresh(comment)

    return comment


def get_comments(
        db: Session,
        post_id: int,
        page_num: int,
        page_size: int
):

    skip = (
        page_num - 1
    ) * page_size

    query = comment_repo.get_post_comments(
        db,
        post_id
    )

    total = query.count()

    records = (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return {
        "records": records,
        "totalRow": total
    }