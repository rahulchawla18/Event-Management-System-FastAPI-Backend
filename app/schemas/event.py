from pydantic import BaseModel, Field
from datetime import datetime

class EventCreate(BaseModel):
    name: str = Field(..., example="Django Meetup")
    location: str = Field(..., example="Bangalore")
    start_time: datetime = Field(..., example="2025-06-29T09:00:00+05:30")
    end_time: datetime = Field(..., example="2025-06-29T12:00:00+05:30")
    max_capacity: int = Field(..., example=100)

class EventOut(BaseModel):
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        orm_mode = True