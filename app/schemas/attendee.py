from pydantic import BaseModel, EmailStr

class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr

class AttendeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
