from typing import Optional
from pydantic import BaseModel
from src.schemas.auth_schema import AuthWithToken, AuthPayload

class MentorBase(BaseModel):
    pass

class MentorAuth(MentorBase):
    email: str
    password: str

class MentorAuthReturn(MentorBase):
    name: str
    email: str
    jwt_token: AuthWithToken

class MentorCreate(MentorBase):
    name: str
    email: str
    password: str
    image_url: Optional[str] = None
    role: Optional[str] = None
    languages: Optional[str] = None
    ig_url: Optional[str] = None
    fb_url: Optional[str] = None
    line_id: Optional[str] = None


class Mentor(MentorBase):
    id: int
    name: str
    email: str
    image_url: Optional[str] = None
    role: Optional[str] = None
    languages: Optional[str] = None
    ig_url: Optional[str] = None
    fb_url: Optional[str] = None
    line_id: Optional[str] = None

    class Config:
        orm_mode = True 