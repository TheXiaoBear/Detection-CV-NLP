from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session

from app.schemas.detect import (
    DetectRequest,
    DetectResponse
)

from app.services.detect import detection


router = APIRouter(
    prefix="/detect",
    tags=["detect"]
)


@router.post(
    "",
    response_model=DetectResponse
)
async def detect(req: DetectRequest, db: Session = Depends(get_db)):

    results = detection(db, req.task_id, req.image_path)

    return {
        "results": results
    }