import json

from sqlalchemy.orm import Session
from llm_app.models.task import Task

from llm_app.services.cv_analysis_service import (
    CVAnalysisService
)

from llm_app.core.prompt_manager import (
    PromptManager
)

from llm_app.core.client import (
    QwenClient
)

from llm_app.repository.report_repo import (
    ReportRepository
)
from llm_app.repository import report_repo
from llm_app.schemas.report import ReportUpdate
from llm_app.rag.rag_service import (
    RAGService
)
from llm_app.services.citation_parser import CitationParser

class ReportService:

    @staticmethod
    def generate(task_id: int, db: Session):

        # =====================
        # 1. task
        # =====================
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        # =====================
        # 2. analysis
        # =====================
        analysis = CVAnalysisService.build(task_id, db)
        if not analysis:
            return None

        analysis_text = json.dumps(
            analysis,
            ensure_ascii=False,
            indent=2
        )

        # =====================
        # 3. RAG（结构化输出）
        # =====================
        knowledge_chunks = RAGService.retrieve(
            query="目标检测 置信度分析 误检优化",
            top_k=3
        )

        knowledge_text = json.dumps(
            knowledge_chunks,
            ensure_ascii=False,
            indent=2
        )

        # =====================
        # 4. Prompt
        # =====================
        messages = [
            {
                "role": "system",
                "content": """
你是计算机视觉专家。

必须遵守：
1. 只能基于 analysis 和 knowledge 推理
2. 禁止编造 Precision / Recall / mAP
3. 样本不足必须说明
4. 每个重要结论尽量标注引用 [chunk_x]
"""
            },
            {
                "role": "user",
                "content": f"""
目标检测统计数据：

{analysis_text}

知识库（结构化）：

{knowledge_text}

请生成完整技术报告（必须包含引用标记）。
"""
            }
        ]

        content = QwenClient.chat(messages)

        # =====================
        # 5. summary
        # =====================
        summary_messages = [
            {
                "role": "system",
                "content": "将报告总结为200字以内，不允许新增信息。"
            },
            {
                "role": "user",
                "content": content
            }
        ]

        try:
            summary = QwenClient.chat(summary_messages)
        except:
            summary = "摘要生成失败"

        # =====================
        # 6. save
        # =====================
        report = ReportRepository.save(
            db=db,
            task_id=task_id,
            title=f"{task.title}_分析报告",
            content=content,
            summary=summary
        )

        task.status = "reported"
        db.commit()

        return report


def report_search(
        db: Session,
        user_id: int,
        page_num: int, page_size: int,
        title: str,
):
    skip = (page_num - 1) * page_size

    return report_repo.report_search(
        db=db,
        user_id=user_id,
        title=title,
        skip=skip,
        page_size=page_size
    )

def update_report(db: Session, report_id: int, report: ReportUpdate):
    return report_repo.update_report(db=db, report_id=report_id, report=report)

def report_delete(db: Session, report_id: int):
    return report_repo.report_delete(db, report_id)