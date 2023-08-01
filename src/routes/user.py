from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header,
    status
)
from src.database.model import (
    Role,
    User,
    Route,
    Access
)
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import user_schemas
from src.services.auth_services import (
    auth_check,
    check_user_by_email,
    pwd_context,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
auth_scheme = HTTPBearer()

router = APIRouter()


@router.post("/signup", response_model=user_schemas.User)
def signup(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user = check_user_by_email(user_data.email, db)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    role = db.query(Role).filter(Role.name == "student").first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found",
        )
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=pwd_context.hash(user_data.password),
        image_url=user_data.image_url,
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_schemas.User(
        id=user.id,
        name=user.name,
        email=user.email,
        image_url=user.image_url,
        created_at=user.created_at,
        role_id=user.role_id,
    )


@router.get("/", response_model=list[user_schemas.User])
@auth_check(route=Route.user, access=Access.read)
async def get_all_student(token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@router.delete("/{id}", response_model=user_schemas.User)
@auth_check(route=Route.user, access=Access.full)
async def delete_student(id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    return user


@router.put("/{id}", response_model=user_schemas.User)
@auth_check(route=Route.user, access=Access.full)
async def update_student(id: int, user_data: user_schemas.UserCreate, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user_data.email:
        user.email = user_data.email
    if user_data.name:
        user.name = user_data.name
    if user_data.image_url:
        user.image_url = user_data.image_url
    db.add(user)
    db.commit()
    return user
