from pydantic import BaseModel
from typing import Optional, List
from src.database.model import Access, Route

class RoleBase(BaseModel):
    pass

class PermissionBase(BaseModel):
    pass

class Permission(PermissionBase):
    id: int
    route: Route
    access: Access

    class Config:
        orm_mode = True

class Role(RoleBase):
    id: int
    name: str
    permissions: List[Permission]

    class Config:
        orm_mode = True

class PermissionCreate(PermissionBase):
    route: str
    access: Access

    class Config:
        orm_mode = True

class RoleCreate(RoleBase):
    name: str
    permissions: List[PermissionCreate]

    class Config:
        orm_mode = True
        
class RoleUpdate(RoleBase):
    name: str
    permissions: List[PermissionCreate]

    class Config:
        orm_mode = True