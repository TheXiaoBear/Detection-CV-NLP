from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from notice_app.db.database import get_db
from notice_app.schemas.notice import NoticeCreate, NoticeCreateResponse
from notice_app.utils.auth import require_admin, get_current_user
from notice_app.utils.security import verify_password
from notice_app.utils.jwt import create_access_token
from notice_app.utils.response import ResponseUtil
from notice_app.utils.page import PageMethod
from notice_app.core.redis_client import redis_client
from typing import Optional, List
import notice_app.service.notice as notice_service
router = APIRouter()

# 新增公告
@router.post("/notice/add", response_model=NoticeCreateResponse)
def notice_add(notice: NoticeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return ResponseUtil.success(data=notice_service.notice_add(db, user_id, notice))

# 删除公告
@router.delete("/notice/{id}", response_model=NoticeCreateResponse)
def notice_delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return ResponseUtil.success(data=notice_service.notice_delete(db, id), message=("notice_deleted by", user_id))

# 修改公告
@router.put("/notice/{id}", response_model=NoticeCreateResponse)
def notice_update(id: int, notice: NoticeCreate,db: Session = Depends(get_db),
                  current_user = Depends(get_current_user)):
    notice.user_id = current_user["user_id"]
    return ResponseUtil.success(data=notice_service.notice_update(db, notice, id))

# 查询 获取 公告
@router.get("/notice/get", response_model=List[NoticeCreateResponse])
def notice_get(db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    page_num: int = 1,
    page_size: int = 10,
    title: str | None = None):

    data = notice_service.notice_search(
        db=db,
        user_id=current_user["user_id"],
        page_num=page_num,
        page_size=page_size,
        title=title
    )

    return ResponseUtil.success(data)