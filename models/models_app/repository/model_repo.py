from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import json
from models_app.models.mixins import TimestampMixin
from models_app.models.model import Model
from models_app.core.redis_client import redis_client

from datetime import datetime, UTC

from models_app.schemas.model import ModelsCreate, ModelsUpdate

def models_search( db: Session,
    model_name: str | None,
    skip: int,
    page_size: int
):
    query = (
        db.query(Model)
    )

    if model_name:
        query = query.filter(
            Model.title.like(f"%{model_name.strip()}%")
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
    # ✅ 正确：先创建 ORM 模型实例
    db_model = Model(**model.model_dump())  # Pydantic v2 用法
    # 如果是 Pydantic v1：Model(**model.dict

    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def models_update(db: Session, model: ModelsUpdate):
    result = db.query(Model).filter(Model.id == model.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Model not found")
    if model.model_name is not None:
        result.model_name = model.model_name
    if model.description is not None:
        result.description = model.description

    db.commit()
    db.refresh(result)
    return result

def activate_model(db: Session, id: int):
    model = db.query(Model).filter(Model.id == id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model.deleted_at = None
    db.commit()
    db.refresh(model)
    return None

def get_model_list(db: Session):
    cache = redis_client.get("model:list")
    if cache:
        return json.loads(cache)

    data = (
        db.query(Model)
        .filter(Model.deleted_at == None)
    )

    total = data.count()
    records = data.all()  # ✅ 执行查询，获取 ORM 对象列表

    serialized_records = [
        {
            "id": item.id,
            "model_name": item.model_name,
            "description": item.description
        }
        for item in records
    ]

    result = {
        "totalRow": total,
        "records": serialized_records
    }

    redis_client.set(
        "model:list",
        json.dumps(result, default=str),
        ex=3600
    )

    return result