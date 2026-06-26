from pydantic import BaseModel, Field, EmailStr


class ModelsResponse(BaseModel):
    id: int
    model_name: str
    description: str

class ModelsCreate(BaseModel):
    model_name: str
    description: str

class ModelsUpdate(BaseModel):
    id: int
    model_name: str
    description: str