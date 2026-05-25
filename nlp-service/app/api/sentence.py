from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.database import get_db

from app.schemas.sentence import (
    GenerateRequest,
    GenerateResponse
)

from app.services.sentence import (
    generate_description
)

router = APIRouter(
    prefix="/generate",
    tags=["generate"]
)


@router.post(
    "",
    response_model=GenerateResponse
)
def generate(
    req: GenerateRequest,
    db: Session = Depends(get_db)
):

    result = generate_description(
        db,
        req.task_id
    )

    return result