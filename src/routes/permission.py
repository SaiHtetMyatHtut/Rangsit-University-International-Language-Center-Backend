from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.schemas import role_schema
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.database.model import Permission, Access, Role

router = APIRouter()


@router.get("/", response_model=list[role_schema.Permission])
async def get_permissions(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    permissions = db.query(Permission).all()
    return permissions


# @router.get("/{role_id}", response_model=list[role_schema.Permission])
# def get_permissions(role_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
#     permissions = db.query(Permission).filter(
#         Permission.role_id == role_id
#     ).all()
#     return permissions


@router.post("/create", response_model=role_schema.Permission)
def create_permission(role_id: int, route_name: str, access: Access, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    permission = Permission(
        route=route_name,
        access=access,
        role_id=role_id
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return role_schema.Permission.from_orm(permission)


@router.delete("/delete", response_model=role_schema.Permission)
def delete_permission(role_id: int, route_name: str, permission_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    role = db.query(Role).filter(Role.id == role_id).first()

    permission = db.query(Permission).filter(
        Permission.route == route_name
    ).filter(
        Permission.role_id == role_id
    ).filter(
        Permission.id == permission_id
    ).first()
    db.delete(permission)
    db.commit()
    return role_schema.Permission.from_orm(permission)
