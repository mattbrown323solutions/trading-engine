from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SystemEventCreate(BaseModel):
    event_type: str = Field(
        min_length=1,
        max_length=100,
    )
    message: str = Field(
        min_length=1,
        max_length=500,
    )


class SystemEventRead(BaseModel):
    id: int
    event_type: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
