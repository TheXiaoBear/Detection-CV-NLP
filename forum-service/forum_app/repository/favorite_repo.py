from forum_app.models.post_favorite import PostFavorite
from sqlalchemy.orm import Session
from forum_app.models.post import Post
from forum_app.models.user import User


def get_favorite(
        db,
        user_id,
        post_id
):
    return (
        db.query(PostFavorite)
        .filter(
            PostFavorite.user_id == user_id,
            PostFavorite.post_id == post_id
        )
        .first()
    )


def create(
        db,
        favorite
):
    db.add(favorite)


def delete(
        db,
        favorite
):
    db.delete(favorite)

def get_favorite_posts(
        db: Session,
        user_id: int
):

    return (
        db.query(
            Post,
            User.username,
            User.avatar
        )
        .join(
            PostFavorite,
            PostFavorite.post_id == Post.id
        )
        .join(
            User,
            User.id == Post.user_id
        )
        .filter(
            PostFavorite.user_id == user_id,
            Post.deleted_at.is_(None)
        )
    )

def is_favorited(
        db: Session,
        user_id: int,
        post_id: int
):
    return (
        db.query(PostFavorite)
        .filter(
            PostFavorite.user_id == user_id,
            PostFavorite.post_id == post_id
        )
        .first()
        is not None
    )