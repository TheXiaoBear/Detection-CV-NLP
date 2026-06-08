from sqlalchemy.orm import Session

from notice_app.models.notice import Notice
from notice_app.schemas.notice import NoticeCreate
from notice_app.repository import notice_repo
from notice_app.utils.security import hash_password, verify_password
from fastapi import HTTPException

from notice_app.utils.page import PageMethod


def notice_add(db: Session, notice: NoticeCreate):
    return notice_repo.notice_add(db, notice)

def notice_delete(db: Session, notice_id: int):
    return notice_repo.notice_delete(db, notice_id)

def notice_update(db: Session, notice, id):
    return notice_repo.notice_update(db, notice, id)

def favorite_search(
    title,
    user_id,
    page_num,
    page_size,
    db: Session
):
    skip = (page_num - 1) * page_size

    return notice_repo.favorite_search(
        db=db,
        user_id=user_id,
        title=title,
        skip=skip,
        page_size=page_size
    )

