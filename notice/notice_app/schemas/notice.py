from pydantic import BaseModel, Field, EmailStr

class NoticeCreate(BaseModel):
    title: str
    content: str

class NoticeCreateResponse(BaseModel):
    user_id: int
    user_name: str
    title: str
    content: str