from pydantic import BaseModel


class GenerateRequest(BaseModel):

    task_id: int


class GenerateResponse(BaseModel):

    task_id: int

    description: str