from functools import wraps
import os
from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database.model import Student, Permission
from src.schemas import student_schema
from src.database.setup import SessionLocal, get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.schemas import auth_schema
from src.schemas import auth_schema
import jwt

# get environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_student_by_email(email: str, db: Session):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        return None
    return student


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(req_student: student_schema.StudentAuth, db: Session):
    student = get_student_by_email(req_student.email, db)

    if not student or not pwd_context.verify(req_student.password, student.hashed_password):
        return None

    return student


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str, db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = auth_schema.TokenData(email = email)
    except JWTError:
        raise credentials_exception
    user = get_student_by_email(email == token_data.email, db)
    if user is None:
        raise credentials_exception
    return user


def auth_check(roles):
    def decorator_auth(func):
        @wraps(func)
        def wrapper_auth(*args, **kwargs):
            print("roles", roles)
            print("args", args)
            print("kwargs", kwargs)
            print(Header("Authorization"))
            db = kwargs["db"]

            return func(*args, **kwargs)
        return wrapper_auth
    return decorator_auth
