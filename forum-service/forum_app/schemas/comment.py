from pydantic import BaseModel, Field


class CommentCreate(BaseModel):

    post_id: int

    content: str = Field(
        ...,
        min_length=1
    )


class CommentResponse(BaseModel):

    id: int

    post_id: int

    user_id: int

    content: str

    class Config:
        from_attributes = True