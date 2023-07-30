from fastapi import APIRouter, Depends

from src.services.auth_services import auth_check
from src.schemas import user_schemas
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.database.model import User, Route, Access
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
auth_scheme = HTTPBearer()

router = APIRouter()


@router.get("/", response_model=list[user_schemas.User])
@auth_check(route=Route.user, access=Access.read)
async def get_all_student(token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.role_id == 2).all()
    return user
