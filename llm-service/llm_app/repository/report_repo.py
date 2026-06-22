from fastapi import HTTPException
from sqlalchemy.orm import Session

from llm_app.models.report import Report
from llm_app.models.task import Task
from llm_app.schemas.report import ReportUpdate

class ReportRepository:

    @staticmethod
    def get_by_task_id(
        db: Session,
        task_id: int
    ):
        return (
            db.query(Report)
            .filter(
                Report.task_id == task_id
            )
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        task_id: int,
        title: str,
        content: str,
        summary: str
    ):
        report = (
            ReportRepository.get_by_task_id(
                db,
                task_id
            )
        )

        # 已存在 -> 更新
        if report:
            report.title = title
            report.content = content
            report.summary = summary

            db.commit()
            db.refresh(report)

            return report

        # 不存在 -> 创建
        report = Report(
            task_id=task_id,
            title=title,
            content=content,
            summary=summary,
        )

        db.add(report)

        db.commit()

        db.refresh(report)

        return report

def report_search(
    db: Session,
    user_id: int,
    title: str | None,
    skip: int,
    page_size: int
):

    query = (
        db.query(Report)
        .join(
            Task,
            Task.id == Report.task_id
        )
        .filter(
            Task.user_id == user_id
        )
    )

    if title:
        query = query.filter(
            Report.title.like(
                f"%{title.strip()}%"
            )
        )

    return (
        query
        .offset(skip)
        .limit(page_size)
        .all()
    )

def update_report(db: Session, report_id: int, report: ReportUpdate):
    result = db.query(Report).filter(Report.id == report_id).first()
    result.title = report.title

    db.commit()
    db.refresh(report)

    return result

def report_delete(db: Session, report_id: int):
    result = db.query(Report).filter(Report.id == report_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(result)
    db.commit()

    return None
