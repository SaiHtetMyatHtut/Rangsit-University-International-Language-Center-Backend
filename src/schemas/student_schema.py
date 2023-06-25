# create pydantic schemas for student with have name, email, hashed_password, image_url, role and id fields.
from typing import Optional
from pydantic import BaseModel
from src.schemas.auth_schema import AuthWithToken, AuthPayload

class StudentBase(BaseModel):
    pass

class StudentAuth(StudentBase):
    email: str
    password: str

class StudentAuthReturn(StudentBase):
    name: str
    email: str
    jwt_token: AuthWithToken

class StudentCreate(StudentBase):
    name: str
    email: str
    password: str
    image_url: Optional[str] = None
    role_id: int


class Student(StudentBase):
    id: int
    name: str
    email: str
    image_url: Optional[str] = None
    role_id: int

    class Config:
        orm_mode = True






