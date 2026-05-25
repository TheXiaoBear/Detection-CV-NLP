from mpmath import limit
from sqlalchemy.orm import Session
from app.models.task import Task
from datetime import datetime, UTC

def create(db: Session, task: Task):
    db.add(task)
    return task


def get_by_id(db: Session, user_id: int, skip=0, limit=100):
    return db.query(Task).filter(
        Task.user_id == user_id,
        Task.deleted_at.is_(None)
    ).offset(skip).limit(limit).first()

def search_title(db: Session, title: str, user_id: int, skip=0, limit=100):
    return db.query(Task).filter(Task.user_id == user_id,
                                 Task.title.like(f"%{title}%"),
                                 Task.deleted_at.is_(None)).offset(skip).limit(limit).first()

def get_all(db: Session, skip=0, limit=100):
    return (
        db.query(Task)
        .filter(Task.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )

def soft_delete(db: Session, task: Task):
    task.deleted_at = datetime.now(UTC)

    return task


def hard_delete(db: Session, task: Task):
    db.delete(task)


def restore_delete(db: Session, task: Task):
    task.deleted_at = None

    return task