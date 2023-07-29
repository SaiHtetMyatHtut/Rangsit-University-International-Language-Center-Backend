from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter
from src.database.model import Student, Role, Permission
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import student_schema
from src.services.auth_services import authenticate_user, get_student_by_email, create_access_token, pwd_context


router = APIRouter()

load_dotenv()  # take environment variables from .env.


# login authentication
@router.get("/login", response_model=student_schema.StudentAuthReturn)
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    student = authenticate_user(student_schema.StudentAuth(
        email=email, password=password), db)
    permissions = db.query(Permission).filter(
        Permission.role_id == student.role_id).all()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    permissions_dict = []
    for permission in permissions:
        permissions_dict.append(permission.route + ":"+permission.access.value)

    # access_token = create_access_token(
    #     data={
    #         "sub": {
    #             "id": student.id,
    #             "name": student.name,
    #             "email": student.email,
    #             "permissions": permissions_dict
    #         }
    #     }
    # )
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
    student = Student(
        name=student_data.name,
        email=student_data.email,
        hashed_password=pwd_context.hash(student_data.password),
        image_url=student_data.image_url,
        role_id=student_data.role_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student_schema.Student(
        id=student.id,
        name=student.name,
        email=student.email,
        image_url=student.image_url,
        role=student.role_id,
    )
