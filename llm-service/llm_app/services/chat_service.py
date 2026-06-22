from sqlalchemy.orm import Session

from llm_app.models.report import Report

from llm_app.rag.rag_service import (
    RAGService
)

from llm_app.core.client import (
    QwenClient
)

from llm_app.repository.chat_repo import (
    ChatRepository
)


class ChatService:

    @staticmethod
    def ask(
        report_id: int,
        question: str,
        db: Session
    ):

        report = (
            db.query(Report)
            .filter(
                Report.id == report_id
            )
            .first()
        )

        if not report:
            return None

        knowledge = (
            RAGService.retrieve(
                question
            )
        )

        knowledge_text = (
            "\n\n".join(
                knowledge
            )
        )

        # history = (
        #     ChatRepository.get_history(
        #         db,
        #         report_id
        #     )
        # )
        history = (
            ChatRepository.get_recent_history(
                db,
                report_id,
                limit=10
            )
        )

        history_text = ""

        for item in history:

            history_text += (
                f"{item.role}: "
                f"{item.content}\n"
            )

        report_context = (
            report.summary
            if report.summary
            else report.content[:2000]
        )
        prompt = f"""
        你是一名计算机视觉专家。

        报告摘要：

        {report_context}

        知识库：

        {knowledge_text}

        历史对话：

        {history_text}

        用户问题：

        {question}

        请结合报告内容和知识库回答。

        如果报告中没有相关证据，
        请明确说明。
        """

        answer = (
            QwenClient.chat(
                prompt
            )
        )

        ChatRepository.save(
            db,
            report_id,
            "user",
            question
        )

        ChatRepository.save(
            db,
            report_id,
            "assistant",
            answer
        )

        return answer

    @staticmethod
    def history(
            report_id: int,
            db: Session
    ):

        return (
            ChatRepository.get_history(
                db,
                report_id
            )
        )