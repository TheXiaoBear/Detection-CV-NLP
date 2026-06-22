from pydantic import BaseModel


class ChatRequest(
    BaseModel
):
    report_id: int
    question: str


class ChatHistoryItem(
    BaseModel
):
    id: int

    role: str

    content: str

    class Config:
        from_attributes = True