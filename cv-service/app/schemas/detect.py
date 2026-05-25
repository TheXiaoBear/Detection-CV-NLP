from pydantic import BaseModel


class DetectRequest(BaseModel):

    task_id: int



class DetectItem(BaseModel):

    label: str

    confidence: float

    x1: float
    y1: float
    x2: float
    y2: float


class DetectResponse(BaseModel):

    task_id: int

    bbox_image: str | None

    heatmap_image: str | None

    results: list[DetectItem]