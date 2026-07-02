from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_app.models.comment import Comment

from forum_app.repository import (
    comment_repo,
    post_repo,
    user_repo
)
from forum_app.services import (
    message_service
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

    current_user = (
        user_repo.get_by_id(
            db,
            user_id
        )
    )

    content = (
        comment_in.content[:30] + "..."
        if len(comment_in.content) > 30
        else comment_in.content
    )

    reply_user_id = None
    parent_comment = None

    # =====================
    # 回复评论
    # =====================
    if comment_in.parent_id:

        parent_comment = (
            comment_repo.get_by_id(
                db,
                comment_in.parent_id
            )
        )

        if not parent_comment:
            raise HTTPException(
                404,
                "评论不存在"
            )

        if parent_comment.post_id != post.id:
            raise HTTPException(
                400,
                "评论数据异常"
            )

        reply_user_id = (
            parent_comment.user_id
        )

    # =====================
    # 创建评论
    # =====================
    comment = Comment(
        post_id=comment_in.post_id,
        user_id=user_id,
        content=comment_in.content,
        parent_id=comment_in.parent_id,
        reply_user_id=reply_user_id
    )

    comment_repo.create(
        db,
        comment
    )

    # 提前获取comment.id
    db.flush()

    # =====================
    # 回复通知
    # =====================
    if parent_comment:

        if parent_comment.user_id != user_id:

            message_service.create_message(
                db,
                parent_comment.user_id,
                "收到回复",
                f"{current_user.username} 回复了你的评论：{content}",
                "reply",
                post.id,
                comment.id,
                parent_comment.id
            )

    # =====================
    # 评论帖子通知
    # =====================
    else:

        if post.user_id != user_id:

            message_service.create_message(
                db,
                post.user_id,
                "帖子收到评论",
                f"{current_user.username} 评论了你的帖子《{post.title}》：{content}",
                "comment",
                post.id
            )

    # =====================
    # 更新统计
    # =====================
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

    rows = (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

    records = []

    for comment, username, avatar, reply_username  in rows:
        records.append({

            "id": comment.id,

            "post_id": comment.post_id,

            "user_id": comment.user_id,

            "parent_id": comment.parent_id,

            "reply_user_id": comment.reply_user_id,

            "content": comment.content,

            "created_at": comment.created_at,

            "username": username,

            "avatar": avatar,
            "reply_username": reply_username

        })

    return {
        "records": records,
        "totalRow": total
    }