from pydantic import BaseModel, Field, EmailStr
from app.schemas.task import TaskResponse


# 入参
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

# 更新用（后面CRUD会用）
class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    avatar: str | None = None


# 出参
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    description: str

    class Config:
        from_attributes = True

class User_to_Task(BaseModel):
    id: int
    username: str
    email: str
    tasks: list[TaskResponse]

    class Config:
        from_attributes = True

# 修改密码
class ChangePassword(BaseModel):
    current_password: str
    new_password: str