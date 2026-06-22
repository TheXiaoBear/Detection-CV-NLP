from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from favorite_app.models.favorite import Favorite
from favorite_app.models.task import Task

from datetime import datetime, UTC

from favorite_app.schemas.favorite import FavoriteCreate
from favorite_app.models.user import User


from favorite_app.models.favorite import Favorite

def favorite_add(
    db: Session,
    user_id: int,
    task_id: int
):
    exists = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == user_id,
            Favorite.task_id == task_id
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="已收藏"
        )

    favorite = Favorite(
        user_id=user_id,
        task_id=task_id
    )

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
        db.query(Task)
        .join(Favorite, Task.id == Favorite.task_id)
        .filter(Favorite.user_id == user_id)
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

def favorite_cancel(db: Session, user_id: int, task_id: int):
    result = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.task_id == task_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(result)
    db.commit()
    return {"message": "取消收藏成功"}