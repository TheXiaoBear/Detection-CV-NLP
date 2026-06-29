from pydantic import BaseModel


class PageMethod(BaseModel):

    page_num: int = 1

    page_size: int = 10