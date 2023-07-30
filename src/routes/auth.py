from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.database.model import User, Role, Permission
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.services.auth_services import authenticate_user, check_user_by_email, create_access_token, pwd_context
from src.schemas import auth_schemas, user_schemas
from src.services import auth_services

router = APIRouter()

load_dotenv()  # take environment variables from .env.


# login authentication
@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(auth_schemas.AuthEmailPassword)],
    db: Session = Depends(get_db),
):
    users = db.query(User).filter(User.email == form_data.email).first()
    if not users:
        return {"error": "Invalid Credentials"}
    user = auth_services.authenticate_user(
        db, form_data.email, form_data.password)
    if not user:
        return {"error": "Invalid Credentials"}
    access_token = auth_services.create_access_token(
        data={"sub": user.email}
    )
    # return {"access_token": access_token, "token_type": "bearer"}

    return user_schemas.UserAuthReturn(
        name=users.name,
        email=users.email,
        jwt_token=user_schemas.AuthWithToken(
            access_token=access_token,
            token_type="bearer",
        ),
    )
