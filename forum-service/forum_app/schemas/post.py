from pydantic import BaseModel, Field


class PostCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    content: str = Field(
        ...,
        min_length=1
    )


class PostUpdate(BaseModel):

    title: str | None = None

    content: str | None = None


class PostResponse(BaseModel):

    id: int

    user_id: int

    title: str

    content: str

    view_count: int

    like_count: int

    comment_count: int

    class Config:
        from_attributes = True