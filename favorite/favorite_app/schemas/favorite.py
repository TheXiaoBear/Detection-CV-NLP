from pydantic import BaseModel, Field, EmailStr
from favorite_app.schemas.task import TaskResponse


class FavoriteCreate(BaseModel):
    task_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    task_id: int

    class Config:
        from_attributes = True

class Favorite_to_Task(BaseModel):
    id: int
    task_id: int
    user_id: int

    task: TaskResponse

    class Config:
        from_attributes = True

class FavoriteCancel(BaseModel):
    task_id: int