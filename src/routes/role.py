from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import role_schema
from src.database.model import Role, Permission, Route, Access
from src.services.auth_services import auth_check

router = APIRouter()


@router.get("/", response_model=list[role_schema.Role])
@auth_check(route=Route.user, access=Access.read)
def get_all_role(db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    roles = db.query(Role).all()
    return roles


@router.get("/{role_id}", response_model=role_schema.Role)
@auth_check(route=Route.user, access=Access.read)
def get_role(role_id: int, db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    return role


@router.post("/create", response_model=role_schema.Role)
@auth_check(route=Route.user, access=Access.write)
def create_role(req_role: role_schema.RoleCreate, db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    role = Role(
        name=req_role.name
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    for permission in req_role.permissions:
        permission = Permission(
            route=permission.route,
            access=permission.access,
            role_id=role.id
        )
        db.add(permission)
        db.commit()
        db.refresh(permission)

    return role_schema.Role(
        id=role.id,
        name=role.name,
        permissions=[role_schema.Permission(
            id=permission.id,
            route=permission.route,
            access=permission.access,
            role_id=permission.role_id
        )]
    )

@router.delete("/delete", response_model=role_schema.Role)
@auth_check(route=Route.user, access=Access.full)
async def delete_role(role_id: int, db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    db.delete(role)
    db.commit()
    return role_schema.Role.from_orm(role)

@router.put("/update", response_model=role_schema.Role)
@auth_check(route=Route.user, access=Access.write)
async def update_role(req_role: role_schema.RoleUpdate, db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    role = db.query(Role).filter(
        Role.id == req_role.id
    ).first()
    role.name = req_role.name
    db.commit()
    db.refresh(role)
    return role_schema.Role.from_orm(role)