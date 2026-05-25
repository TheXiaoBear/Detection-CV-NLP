# app/services/task.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.task import Task
from app.schemas.task import TaskUpdate
from app.repository import task_repo
from app.utils.page import PageMethod
from app.repository.task_repo import search_title


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

def get_task(title, user_id: int, page: PageMethod, db: Session):
    skip = (page.page_num - 1) * page.page_size
    if title is None:
        task = task_repo.get_by_id(db, user_id, skip=skip, limit=page.page_size)
    if title:
        task = search_title(db, title, user_id, skip=skip, limit=page.page_size)

    if not task:
        raise HTTPException(404, "Task not found")

    return task


def get_tasks(page: PageMethod ,db: Session):
    skip = (page.page_num - 1) * page.page_size
    return task_repo.get_all(db, skip=skip, limit=page.page_size)


def update_task(db: Session, task_id: int, task_in: TaskUpdate):

    task = get_task(db, task_id)

    if task_in.status:
        task.status = task_in.status

    db.commit()
    db.refresh(task)

    return task


def soft_delete_task(db: Session, task_id: int):

    task = get_task(db, task_id)

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

