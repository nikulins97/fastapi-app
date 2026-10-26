from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


AnalysisStatus = Literal[
    "pending",
    "processing",
    "completed",
    "failed",
]

class AnalysisCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    image_url: HttpUrl


class AnalysisUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    status: AnalysisStatus | None = None
    result: str | None = None


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image_url: HttpUrl
    status: AnalysisStatus
    result: str | None
    created_at: datetime