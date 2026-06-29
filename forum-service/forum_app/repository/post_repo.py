from sqlalchemy.orm import Session

from forum_app.models.post import Post


# 新建帖子
def create(
        db: Session,
        post: Post
):
    db.add(post)

    return post


# 根据id查询
def get_by_id(
        db: Session,
        post_id: int
):
    return (
        db.query(Post)
        .filter(
            Post.id == post_id,
            Post.deleted_at.is_(None)
        )
        .first()
    )


# 获取所有帖子
def get_all(
        db: Session
):
    return (
        db.query(Post)
        .filter(
            Post.deleted_at.is_(None)
        )
    )


# 搜索帖子
def search(
        db: Session,
        keyword: str
):
    return (
        db.query(Post)
        .filter(
            Post.title.like(f"%{keyword}%"),
            Post.deleted_at.is_(None)
        )
    )


# 获取我的帖子
def get_by_user_id(
        db: Session,
        user_id: int
):
    return (
        db.query(Post)
        .filter(
            Post.user_id == user_id,
            Post.deleted_at.is_(None)
        )
    )


# 删除帖子
def delete(
        db: Session,
        post: Post
):
    db.delete(post)