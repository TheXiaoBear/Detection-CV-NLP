from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models_app.models.mixins import TimestampMixin
from models_app.models.model import Model
from models_app.models.task import Task

from datetime import datetime, UTC

from models_app.schemas.model import ModelsCreate

def favorite_search( db: Session,
    model_name: str | None,
    skip: int,
    page_size: int
):
    query = (
        db.query(Model)
        .filter(Model.deleted_at.is_(None))
    )

    if model_name:
        query = query.filter(
            Task.title.like(f"%{model_name.strip()}%")
        )

    return (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

def stop_model(db: Session, id: int):
    model = Model.query.get(id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model.deleted_at = datetime.now()
    db.add(model)
    db.commit()
    db.refresh(model)
    return None

def models_add(db: Session, model: ModelsCreate):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model