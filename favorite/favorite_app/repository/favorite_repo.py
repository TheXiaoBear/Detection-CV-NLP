from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from favorite_app.models.favorite import Favorite
from favorite_app.models.task import Task

from datetime import datetime, UTC

from favorite_app.schemas.favorite import FavoriteCreate
from models.user import User


def favorite_add(db: Session, favorite: FavoriteCreate):
    db.add(favorite)
    db.commit()

    db.refresh(favorite)

    return favorite

def favorite_search(
    db: Session,
    user_id: int,
    title: str | None,
    skip: int,
    page_size: int
):
    query = (
        db.query(Favorite)
        .join(Task, Favorite.task_id == Task.id)
        .options(joinedload(Favorite.task))
        .filter(Favorite.user_id == user_id)
    )

    if title:
        query = query.filter(
            Task.title.like(f"%{title.strip()}%")
        )

    return (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

def favorite_cancel(db: Session, user_id: int, task_id: int):
    result = db.query(Favorite).filter(Favorite.task_id == task_id).first()
    if result:
        raise HTTPException(status_code=404, detail="Favorite already canceled")

    db.delete(result)

    db.commit()
    db.refresh(result)
    return result