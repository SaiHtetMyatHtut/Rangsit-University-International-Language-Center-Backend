from functools import wraps
import os
from jose import jwt, JWTError
from datetime import (
    datetime,
    timedelta
)
from passlib.context import CryptContext
from src.database.model import (
    User,
    Role,
    Permission,
    Route,
    Access
)
from src.database.setup import get_db
from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from sqlalchemy.orm import Session


# get environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Error Handling
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# check user by email


def check_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user if user else None


def authenticate_user(db, email: str, password: str):
    user = check_user_by_email(email=email, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: str = None):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"sub": email}
    except JWTError:
        raise credentials_exception
    user = check_user_by_email(email == token_data.email, db=db)
    if user is None:
        raise credentials_exception
    return user

# Decorator for checking authentication
def auth_check(route: Route, access: Access):
    def decorator_auth(func):
        @wraps(func)
        async def wrapper_auth(*args, **kwargs):
            db = kwargs["db"]
            token = kwargs["token"]
            permission = route.value+":"+access.value

            decoded_token = jwt.decode(
                token=token.credentials,
                key=SECRET_KEY,
                algorithms=[ALGORITHM]

            )
            user = db.query(User).filter(
                User.email == decoded_token["sub"]
            ).first()

            role = db.query(Role).filter(Role.id == user.role_id).first()

            accesses = []

            for x in role.permissions:
                accesses.append(x.route.value+":"+x.access.value)

            if permission not in accesses:
                raise HTTPException(
                    status_code=403, detail="You don't have permission to access this resource")
            return await func(*args, **kwargs)
        return wrapper_auth
    return decorator_auth
