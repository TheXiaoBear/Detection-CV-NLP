from pydantic import BaseModel


class TaskCreate(BaseModel):
    user_id: int


class TaskUpdate(BaseModel):
    status: str | None = None
    title: str


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    image_path: str
    status: str

    class Config:
        from_attributes = True

class StartTaskRequest(BaseModel):
    model_name: str