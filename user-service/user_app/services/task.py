# user_app/services/task.py

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from user_app.models.task import Task
from user_app.schemas.task import TaskUpdate
from user_app.repository import task_repo
from user_app.utils.page import PageMethod
from user_app.repository.task_repo import search_title


def create_task(
    db: Session,
    user_id: int,
    title: str | None = None,
    image_path: str | None = None,
    status: str = "pending",
):

    task = Task(
        user_id=user_id,
        image_path=image_path,
        status="pending"
    )

    try:
        task_repo.create(db, task)
        db.flush()

        if title is None:
            task.title = str(task.id)

        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise

def get_task(title, user_id, page_num, page_size, db: Session):

    skip = (page_num - 1) * page_size

    query = db.query(Task).filter(
        Task.user_id == user_id,
        Task.deleted_at.is_(None)
    )

    if title is not None and title.strip() != "":
        query = query.filter(Task.title.like(f"%{title.strip()}%"))

    total = query.count()

    records = query.options(
        joinedload(Task.favorites)
    ).offset(skip).limit(page_size).all()

    result = []
    for task in records:
        is_favorited = any(
            fav.user_id == user_id for fav in task.favorites
        )
        result.append({
            **task.__dict__,
            "is_favorited": is_favorited
        })

    return {
        "records": result,
        "totalRow": total
    }

def get_tasks(page: PageMethod ,db: Session):
    skip = (page.page_num - 1) * page.page_size
    return task_repo.get_all(db, skip=skip, limit=page.page_size)


def update_task(db: Session, task_id: int, task_in: TaskUpdate):

    task = db.query(Task).filter(Task.id == task_id).first()

    if task_in.status:
        task.status = task_in.status

    if task_in.title:
        task.title = task_in.title

    db.commit()
    db.refresh(task)

    return task

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id,
        Task.deleted_at.is_(None)).first()

def soft_delete_task(db: Session, task_id: int):

    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    task_repo.soft_delete(db, task)

    db.commit()
    db.refresh(task)

    return task


def search_task_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def hard_delete_task(db: Session, task_id: int):

    task = search_task_id(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    task_repo.hard_delete(db, task)

    db.commit()

def restore_delete_task(db: Session, task_id: int):

    task = search_task_id(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    task_repo.restore_delete(db, task)

    db.commit()
    db.refresh(task)

    return task

def get_tasks_delete(page: PageMethod, user_id ,db: Session):
    skip = (page.page_num - 1) * page.page_size
    result = db.query(Task).filter(Task.deleted_at.isnot(None), Task.user_id == user_id).offset(skip).limit(page.page_size).all()
    return result


def task_result(db: Session, task_id: int):
    result = task_repo.search_task_result(db, task_id)
    return result

def get_delete_task(title, user_id, page_num, page_size, db: Session):

    skip = (page_num - 1) * page_size

    query = db.query(Task).filter(
        Task.user_id == user_id,
        Task.deleted_at.isnot(None)
    )

    if title is not None and title.strip() != "":
        query = query.filter(Task.title.like(f"%{title.strip()}%"))

    total = query.count()

    records = query.offset(skip).limit(page_size).all()

    return {
        "records": records,
        "totalRow": total
    }