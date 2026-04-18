from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ProfileCreate(BaseModel):
    name : str = Field(...,min_length=1,description="The first name to analyze")

class ProfileResponse(BaseModel):
    id: str
    name: str
    gender: str
    gender_probability: float
    sample_size: int
    age: int
    age_group: str
    country_id: str
    country_probability: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    status:str = "success"
    message: str
    data: ProfileResponse

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str