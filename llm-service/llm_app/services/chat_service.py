from sqlalchemy.orm import Session

from llm_app.models.report import Report
from llm_app.rag.rag_service import RAGService
from llm_app.core.client import QwenClient
from llm_app.repository.chat_repo import ChatRepository


class ChatService:

    @staticmethod
    def ask(
        report_id: int,
        question: str,
        db: Session
    ):
        """
        非流式版本
        """

        report = (
            db.query(Report)
            .filter(Report.id == report_id)
            .first()
        )

        if not report:
            return None

        # =========================
        # RAG
        # =========================
        knowledge = RAGService.retrieve(question)

        knowledge_text_list = []

        for item in knowledge:

            if isinstance(item, dict):

                knowledge_text_list.append(
                    item.get("text", "")
                )

            elif isinstance(item, str):

                knowledge_text_list.append(item)

        knowledge_text = "\n\n".join(
            knowledge_text_list
        )

        # =========================
        # 历史记录
        # =========================
        history = ChatRepository.get_recent_history(
            db,
            report_id,
            limit=10
        )

        history_text = ""

        for item in history:
            history_text += (
                f"{item.role}: "
                f"{item.content}\n"
            )

        # =========================
        # 报告内容
        # =========================
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

        answer = QwenClient.chat(prompt)

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

    # ==================================
    # 流式版本
    # ==================================
    @staticmethod
    def stream_ask(
        report_id: int,
        question: str,
        db: Session
    ):
        print("==========进入 stream_ask==========")

        report = (
            db.query(Report)
            .filter(Report.id == report_id)
            .first()
        )

        if not report:
            yield "report not found"
            return

        # =========================
        # RAG
        # =========================
        knowledge = RAGService.retrieve(question)

        knowledge_text_list = []

        for item in knowledge:

            if isinstance(item, dict):

                knowledge_text_list.append(
                    item.get("text", "")
                )

            elif isinstance(item, str):

                knowledge_text_list.append(item)

        knowledge_text = "\n\n".join(
            knowledge_text_list
        )

        # =========================
        # 历史记录
        # =========================
        history = ChatRepository.get_recent_history(
            db,
            report_id,
            limit=10
        )

        history_text = ""

        for item in history:
            history_text += (
                f"{item.role}: "
                f"{item.content}\n"
            )

        # =========================
        # 报告内容
        # =========================
        report_context = (
            report.summary
            if report.summary
            else report.content[:2000]
        )

        messages = [
            {
                "role": "system",
                "content": """
        你是一名计算机视觉专家。

        请结合报告内容和知识库回答。

        如果报告中没有相关证据，
        请明确说明。
        """
            },
            {
                "role": "user",
                "content": f"""
        报告摘要：
        {report_context}

        知识库：
        {knowledge_text}

        历史对话：
        {history_text}

        用户问题：
        {question}
        """
            }
        ]

        full_answer = ""

        try:

            print("开始调用大模型")
            # 如果 stream_chat 接收字符串
            for chunk in QwenClient.stream_chat(messages):

                if not chunk:
                    continue

                full_answer += chunk

                yield chunk
                print("流式结束")

        except Exception as e:

            print("stream error:", str(e))

            yield f"\n\n[ERROR] {str(e)}"

        finally:

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
                full_answer
            )

    @staticmethod
    def history(
        report_id: int,
        db: Session
    ):
        return ChatRepository.get_history(
            db,
            report_id
        )