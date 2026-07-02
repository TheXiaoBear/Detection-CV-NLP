from pydantic import BaseModel


class FeedbackCreate(BaseModel):

    title: str

    content: str

    feedback_type: str


class FeedbackReply(BaseModel):

    admin_reply: str