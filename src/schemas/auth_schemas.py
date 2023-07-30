from typing import Union
from pydantic import BaseModel


class AuthWithToken(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        orm_mode = True


class AuthEmailPassword(BaseModel):
    email: str
    password: str


class AuthPayload(BaseModel):
    sub: str
    exp: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class PermissionData(BaseModel):
    route: str
    access: str
