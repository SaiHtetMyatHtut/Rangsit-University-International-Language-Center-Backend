import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.database.model import Student
from src.database.setup import get_db
from sqlalchemy.orm import Session

from src.schemas import student_schema

router = APIRouter()

load_dotenv()  # take environment variables from .env.

# get environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# login authentication


@router.post("/login", response_model=student_schema.StudentAuthReturn)
def login(req_student: student_schema.StudentAuth, db: Session = Depends(get_db)):
    student = authenticate_user(req_student, db)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": student.email})

    return student_schema.StudentAuthReturn(
        name=student.name,
        email=student.email,
        jwt_token=student_schema.AuthWithToken(
            access_token=access_token, token_type="bearer"
        ),
    )


# signup authentication
@router.post("/signup", response_model=student_schema.Student)
def signup(student_data: student_schema.StudentCreate, db: Session = Depends(get_db)):
    student = get_student_by_email(student_data.email, db)
    if student is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    student = Student(name=student_data.name, email=student_data.email,
                      hashed_password=pwd_context.hash(student_data.password))
    db.add(student)
    db.commit()
    db.refresh(student)
    return student_schema.Student(
        id=student.id,
        name=student.name,
        email=student.email,
        image_url=student.image_url,
        role=student.role,
    )


def get_student_by_email(email: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        return None
    return student


def authenticate_user(req_student: student_schema.StudentAuth, db: Session = Depends(get_db)):
    student = get_student_by_email(req_student.email, db)

    if not student or not pwd_context.verify(req_student.password, student.hashed_password):
        return None

    return student


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def jwt_bearer_auth(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )

    user = get_student_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )

    return user


# Sample Request Body
# {
#   "email": "sai@gmail.com",
#   "password": "12345"
# }

# Sample Request Body
# {
#   "name": "Sai",
#   "email": "sai@gmail.com",
#   "password": "12345",
#   "image_url":"",
#   "role":""
# }
