# create pydantic schemas for student with have name, email, hashed_password, image_url, role and id fields.
from typing import Optional
from pydantic import BaseModel


class StudentBase(BaseModel):
    email: str

class StudentCreate(StudentBase):
    name: str
    password: str
    image_url: Optional[str] = None
    role: Optional[str] = None

class StudentLogIn(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    name: str
    image_url: Optional[str] = None
    role: Optional[str] = None
    class Config:
        orm_mode = True

