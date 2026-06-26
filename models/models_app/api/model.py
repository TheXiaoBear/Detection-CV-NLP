from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from models_app.db.database import get_db
from models_app.schemas.model import ModelsResponse, ModelsCreate, ModelsUpdate
from models_app.utils.auth import require_admin, get_current_user

from models_app.utils.response import ResponseUtil
from models_app.utils.page import PageMethod
from models_app.core.redis_client import redis_client
from typing import Optional, List
import models_app.service.model as model_service
router = APIRouter()

# 获取模型
@router.get("/models/get")
def get_models(db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    page_num: int = 1,
    page_size: int = 10,
    model_name: str | None = None):

    data = model_service.get_models(db=db,
        page_num=page_num,
        page_size=page_size,
        model_name=model_name)

    return ResponseUtil.success(data)

# 删 | 禁用 模型
@router.put("/models/stop/{id}")
def stop_model(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return ResponseUtil.success(model_service.stop_model(db=db, id=id), message="Model stopped")

# 新增模型
@router.post("/models/add", response_model=ModelsResponse)
def models_add(model: ModelsCreate, db: Session = Depends(get_db)):
    return ResponseUtil.success(model_service.models_add(db=db, model=model))

# 更新模型信息
@router.put("/models/change/{id}")
def models_update(model: ModelsUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return ResponseUtil.success(model_service.models_update(db=db, model=model))

# 启用模型
@router.put("/models/activate/{id}")
def activate_model(id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return ResponseUtil.success(model_service.activate_model(db=db, id=id) ,message="Model activated")

# 获取模型列表
@router.get("/models/list")
def get_model_list(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ResponseUtil.success(model_service.get_model_list(db=db))