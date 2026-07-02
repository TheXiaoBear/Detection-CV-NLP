from pydantic import BaseModel


class PageMethod(BaseModel):
    page_num: int
    page_size: int


