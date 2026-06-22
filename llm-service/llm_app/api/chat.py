from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from llm_app.db.database import (
    get_db
)

from llm_app.schemas.chat import (
    ChatRequest
)

from llm_app.services.chat_service import (
    ChatService
)
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/ask")
def ask(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    answer = (
        ChatService.ask(
            request.report_id,
            request.question,
            db
        )
    )

    if not answer:

        return {
            "code": 404,
            "message": "报告不存在"
        }

    return {
        "code": 200,
        "message": "success",
        "data": answer
    }


@router.get(
    "/history/{report_id}"
)
def history(
    report_id: int,
    db: Session = Depends(get_db)
):

    messages = (
        ChatService.history(
            report_id,
            db
        )
    )

    return {
        "code": 200,
        "message": "success",
        "data": messages
    }

@router.post("/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    return StreamingResponse(
        ChatService.stream_ask(
            request.report_id,
            request.question,
            db
        ),
        media_type="text/plain"
    )