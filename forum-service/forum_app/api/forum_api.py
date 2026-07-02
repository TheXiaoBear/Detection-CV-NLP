from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from forum_app.db.database import get_db

from forum_app.utils.response import ResponseUtil

from forum_app.utils.auth import (
    get_current_user
)

from forum_app.schemas.post import (
    PostCreate,
    PostUpdate
)

from forum_app.schemas.comment import (
    CommentCreate
)

from forum_app.services import (
    message_service
)

from forum_app.services import (
    post_service,
    comment_service,
    like_service,
    favorite_post
)

router = APIRouter()

# 发帖
@router.post("/posts")
def create_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):
    result = post_service.create_post(
        db,
        current_user["user_id"],
        post
    )

    return ResponseUtil.success(
        data=result,
        message="发帖成功"
    )

# 帖子详情
@router.get("/posts/{post_id}")
def get_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = post_service.get_post(
        db,
        post_id,
        current_user["user_id"]
    )

    return ResponseUtil.success(
        data=result
    )

# 修改帖子
@router.put("/posts/{post_id}")
def update_post(
        post_id: int,
        post: PostUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = post_service.update_post(
        db,
        current_user["user_id"],
        post_id,
        post
    )

    return ResponseUtil.success(
        data=result,
        message="修改成功"
    )

# 删除帖子
@router.delete("/posts/{post_id}")
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    post_service.delete_post(
        db,
        current_user["user_id"],
        post_id
    )

    return ResponseUtil.success(
        message="删除成功"
    )

# 帖子列表
@router.get("/posts")
def list_posts(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
):

    result = post_service.get_posts(
        db,
        page_num,
        page_size
    )

    return ResponseUtil.success(
        data=result
    )

# 搜索帖子
@router.get("/posts_search")
def search_post(
        keyword: str,
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
):

    result = post_service.search_post(
        db,
        keyword,
        page_num,
        page_size
    )

    return ResponseUtil.success(
        data=result
    )

# 我的帖子
@router.get("/my/posts")
def my_posts(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = post_service.my_posts(
        db,
        current_user["user_id"],
        page_num,
        page_size
    )

    return ResponseUtil.success(
        data=result
    )

# 评论
@router.post("/comments")
def create_comment(
        comment: CommentCreate,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = comment_service.create_comment(
        db,
        current_user["user_id"],
        comment
    )

    return ResponseUtil.success(
        data=result,
        message="评论成功"
    )

# 评论列表
@router.get("/comments/{post_id}")
def get_comments(
        post_id: int,
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
):

    result = comment_service.get_comments(
        db,
        post_id,
        page_num,
        page_size
    )

    return ResponseUtil.success(
        data=result
    )

# 点赞
@router.post("/posts/{post_id}/like")
def toggle_like(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = like_service.toggle_like(
        db,
        current_user["user_id"],
        post_id
    )

    return ResponseUtil.success(
        data=result
    )

@router.post(
    "/posts/{post_id}/favorite"
)
def toggle_favorite(
        post_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = (
        favorite_post
        .toggle_favorite(
            db,
            current_user["user_id"],
            post_id
        )
    )

    return ResponseUtil.success(
        data=result
    )

@router.get("/my/favorites")
def my_favorites(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = (
        favorite_post.my_favorites(
            db,
            current_user["user_id"],
            page_num,
            page_size
        )
    )

    return ResponseUtil.success(
        data=result
    )

@router.get("/my/favorites")
def my_favorites(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = (
        favorite_post.my_favorites(
            db,
            current_user["user_id"],
            page_num,
            page_size
        )
    )

    return ResponseUtil.success(
        data=result
    )

@router.get("/messages")
def my_messages(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = (
        message_service.my_messages(
            db,
            current_user["user_id"],
            page_num,
            page_size
        )
    )

    return ResponseUtil.success(
        data=result
    )

@router.put(
    "/messages/{message_id}/read"
)
def read_message(
        message_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    result = (
        message_service.read_message(
            db,
            current_user["user_id"],
            message_id
        )
    )

    return ResponseUtil.success(
        data=result
    )

@router.get("/messages/unread/count")
def unread_count(
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    return ResponseUtil.success(
        data=
        message_service.unread_count(
            db,
            current_user["user_id"]
        )
    )

@router.put("/messages/read/all")
def read_all_messages(
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    message_service.read_all_messages(
        db,
        current_user["user_id"]
    )

    return ResponseUtil.success(
        message="全部已读"
    )