from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.schemas.auth_schemas import AuthWithToken


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    name: str
    email: str
    password: str
    image_url: Optional[str] = None
    is_active: bool = True



class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    hashed_password: Optional[str] = None


class UserDelete(UserBase):
    id: int


class UserAuth(UserBase):
    email: str
    password: str


class UserAuthReturn(UserBase):
    name: str
    email: str
    jwt_token: AuthWithToken

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    name: str
    email: str
    image_url: Optional[str] = None
    created_at: datetime
    role_id: int

    class Config:
        orm_mode = True
