from pydantic import BaseModel, Field, EmailStr
from favorite_app.schemas.task import TaskResponse

class NoticeCreate(BaseModel):
    user_id: int
    user_name: str
    title: str
    content: str

class NoticeCreateResponse(BaseModel):
    user_id: int
    user_name: str
    title: str
    content: str