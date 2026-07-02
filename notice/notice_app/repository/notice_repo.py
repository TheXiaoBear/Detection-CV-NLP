from fastapi import HTTPException
from openai.resources.skills import content
from sqlalchemy.orm import Session, joinedload
from sympy.parsing.sympy_parser import null

from notice_app.models.notice import Notice
from notice_app.models.task import Task

from datetime import datetime, UTC

from notice_app.schemas.notice import NoticeCreate
from notice_app.models.user import User

def notice_add(db: Session, user_id: int, notice: NoticeCreate):
    user_name = db.query(User).filter(User.id == user_id).first().username
    notice_new = Notice(user_id=user_id, user_name=user_name,
                        title=notice.title, content=notice.content)
    db.add(notice_new)

    db.commit()
    db.refresh(notice_new)
    return notice_new

def notice_delete(db: Session, notice_id: int):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(400, "公告不存在")
    db.delete(notice)
    db.commit()
    db.refresh(notice)
    return null
def notice_update(db: Session, notice: NoticeCreate, id: int):
    notice_now = db.query(Notice).filter(Notice.id == id).first()
    if not notice:
        raise HTTPException(400, "公告不存在")
    if notice.user_id : notice_now.user_id = notice.user_id
    if notice.title : notice_now.title = notice.title
    if notice.content : notice_now.content = notice.content
    if notice.user_name : notice_now.user_name = notice.user_name

    db.commit()
    db.refresh(notice_now)
    return notice_now

def notice_search(
    db: Session,
    title: str | None,
    skip: int,
    page_size: int
):
    query = (
        db.query(Notice)
    )

    if title:
        query = query.filter(
            Task.title.like(f"%{title.strip()}%")
        )

    total = query.count()

    records = (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return {
        "totalRow": total,
        "records": records
    }