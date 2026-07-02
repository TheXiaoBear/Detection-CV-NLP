from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from feedback_app.db.database import (
    get_db
)

from feedback_app.schemas.feedback import (
    FeedbackCreate,
    FeedbackReply
)

from feedback_app.services import (
    feedback_service
)

from feedback_app.utils.auth import (
    get_current_user,
    require_admin
)
from feedback_app.utils.response import ResponseUtil

router = APIRouter(
    prefix="/feedback",
    tags=["反馈中心"]
)

@router.post("")
def create_feedback(
        feedback: FeedbackCreate,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    return ResponseUtil.success(
        feedback_service.create_feedback(
            db,
            current_user["user_id"],
            feedback
        )
    )

@router.get("/my")
def my_feedback(
        page_num: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    return ResponseUtil.success(
        feedback_service.my_feedback(
            db,
            current_user["user_id"],
            page_num,
            page_size
        )
    )


@router.get("/admin/list")
def get_feedback_list(
        page_num: int = 1,
        page_size: int = 10,
        status: str = None,
        db: Session = Depends(get_db),
        current_admin=Depends(
            require_admin
        )
):
    return ResponseUtil.success(
        feedback_service.get_feedback_list(
            db,
            page_num,
            page_size,
            status
        )
    )


@router.get("/admin/{feedback_id}")
def admin_feedback_detail(
        feedback_id: int,
        db: Session = Depends(get_db),
        current_admin=Depends(
            require_admin
        )
):

    return ResponseUtil.success(
        feedback_service.admin_feedback_detail(
            db,
            feedback_id
        )
    )

@router.get("/{feedback_id}")
def get_feedback_detail(
        feedback_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(
            get_current_user
        )
):

    return ResponseUtil.success(
        feedback_service.get_feedback_detail(
            db,
            feedback_id,
            current_user["user_id"]
        )
    )

@router.put("/admin/{feedback_id}")
def reply_feedback(
        feedback_id: int,
        reply: FeedbackReply,
        db: Session = Depends(get_db),
        current_admin=Depends(
            require_admin
        )
):

    return ResponseUtil.success(
        feedback_service.reply_feedback(
            db,
            feedback_id,
            reply
        )
    )