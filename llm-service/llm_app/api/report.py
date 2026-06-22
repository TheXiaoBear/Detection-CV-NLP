from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from llm_app.db.database import get_db
from llm_app.utils.auth import require_admin, get_current_user
from llm_app.schemas.report import ReportUpdate

from llm_app.utils.response import ResponseUtil
from llm_app.services.report import (
    ReportService
)
import llm_app.services.report as report_service

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.post(
    "/generate/{task_id}"
)
def generate_report(
    task_id: int,
    db: Session = Depends(get_db)
):
    report = (
        ReportService.generate(
            task_id,
            db
        )
    )

    if not report:

        return {
            "code": 404,
            "message": "未找到检测结果"
        }

    return {
        "code": 200,
        "message": "报告生成成功",
        "data": {
            "report_id": report.id,
            "task_id": report.task_id,
            "content": report.content,
            "summary": report.summary,
        }
    }

# 查询报告
@router.get("/generate")
def report_search(db: Session = Depends(get_db),
    # current_user = Depends(get_current_user),
    page_num: int = 1,
    page_size: int = 10,
    title: str | None = None):

    data = report_service.report_search(
        db=db,
        user_id=1,
        page_num=page_num,
        page_size=page_size,
        title=title
    )

    return ResponseUtil.success(data)

@router.put("/generate/{report_id}")
def report_update(
    report_id: int,
    report_update: ReportUpdate,
    db: Session = Depends(get_db),
):
    return ResponseUtil.success(report_service.update_report(db, report_id, report_update))

@router.delete("/generate/{report_id}")
def report_delete(
    report_id: int,
    db: Session = Depends(get_db),
):

    return ResponseUtil.success(data= report_service.report_delete(db, report_id),message="删除成功")