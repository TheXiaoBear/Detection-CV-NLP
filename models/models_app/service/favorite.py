from sqlalchemy.orm import Session

from favorite_app.models.favorite import Favorite
from favorite_app.schemas.favorite import FavoriteCreate
from favorite_app.repository import favorite_repo
from favorite_app.utils.security import hash_password, verify_password
from fastapi import HTTPException

from favorite_app.utils.page import PageMethod

# 新增收藏
def favorite_add(db: Session, favorite: FavoriteCreate):
    return favorite_repo.favorite_add(db, favorite)

# 搜索或展示收藏
def favorite_search(
    title,
    user_id,
    page_num,
    page_size,
    db: Session
):
    skip = (page_num - 1) * page_size

    return favorite_repo.favorite_search(
        db=db,
        user_id=user_id,
        title=title,
        skip=skip,
        page_size=page_size
    )

def favorite_cancel(db: Session, user_id: int, task_id: int):
    return favorite_repo.favorite_cancel(db=db, user_id=user_id, task_id=task_id)