from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cv_app.db.database import get_db

from cv_app.utils.response import ResponseUtil

from cv_app.schemas.detect import (
    DetectRequest,
    DetectResponse
)

from cv_app.services.detect import detection

from cv_app.core.manager import ModelManager


router = APIRouter(
    prefix="/detect",
    tags=["detect"]
)


@router.post(
    "",
    response_model=DetectResponse
)
async def detect(
    req: DetectRequest,
    db: Session = Depends(get_db)
):

    results = detection(
        db,
        req.task_id,
        req.model_name
    )

    return ResponseUtil.success(results)


@router.get("/models")
async def get_models():

    return ResponseUtil.success({

        "current_model": ModelManager.get_current_model_name(),

        "loaded_models": ModelManager.get_loaded_models(),

        "available_models": ModelManager.get_available_models()
    })