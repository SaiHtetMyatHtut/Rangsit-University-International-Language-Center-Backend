from fastapi import APIRouter, Depends
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import role_schema
from src.database.model import Role, Permission

router = APIRouter()


@router.get("/", response_model=list[role_schema.Role])
def get_all_role(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@router.get("/{role_id}", response_model=role_schema.Role)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    return role_schema.Role.from_orm(role)


@router.post("/create", response_model=role_schema.Role)
def create_role(req_role: role_schema.RoleCreate, db: Session = Depends(get_db)):
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
