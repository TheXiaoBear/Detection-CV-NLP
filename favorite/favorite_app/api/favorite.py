from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from favorite_app.db.database import get_db
from favorite_app.schemas.favorite import FavoriteCreate, FavoriteResponse, Favorite_to_Task, FavoriteCancel
from favorite_app.utils.auth import require_admin, get_current_user
from favorite_app.utils.security import verify_password
from favorite_app.utils.jwt import create_access_token
from favorite_app.utils.response import ResponseUtil
from favorite_app.utils.page import PageMethod
from favorite_app.core.redis_client import redis_client
from typing import Optional, List
import favorite_app.service.favorite as favorite_service
router = APIRouter()

# 添加收藏
@router.post("/add")
def favorite_add(
    favorite: FavoriteCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return ResponseUtil.success(
        favorite_service.favorite_add(
            db=db,
            user_id=current_user["user_id"],
            task_id=favorite.task_id
        )
    )

# 搜索收藏内容
@router.get("/list")
def favorite_list(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    page_num: int = 1,
    page_size: int = 10,
    title: str | None = None
):
    data = favorite_service.favorite_search(
        db=db,
        user_id=current_user["user_id"],
        page_num=page_num,
        page_size=page_size,
        title=title
    )

    return ResponseUtil.success(data)

# 取消收藏
@router.put("/cancel", response_model=FavoriteResponse)
def favorite_cancel(data: FavoriteCancel, db: Session = Depends(get_db),
                    current_user = Depends(get_current_user),
                    ):
    data = favorite_service.favorite_cancel(db=db, user_id=current_user.id, task_id=data.task_id)