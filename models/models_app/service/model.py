from sqlalchemy.orm import Session

from models_app.models.model import Model
from models_app.schemas.model import ModelsCreate, ModelsUpdate
from models_app.repository import model_repo
from fastapi import HTTPException

def get_models(model_name,
    page_num,
    page_size,
    db: Session):

    skip = (page_num - 1) * page_size

    return model_repo.models_search(
        db=db,
        model_name=model_name,
        skip=skip,
        page_size=page_size
    )

def stop_model(db: Session, id: int):

    return model_repo.stop_model(db=db, id=id)

def models_add(db: Session, model: ModelsCreate):
    return model_repo.models_add(db=db, model=model)

def models_update(db: Session, model: ModelsUpdate):
    return model_repo.models_update(db=db, model=model)

def activate_model(db: Session, id: int):
    return model_repo.activate_model(db=db, id=id)

def get_model_list(db: Session):
    return model_repo.get_model_list(db=db)