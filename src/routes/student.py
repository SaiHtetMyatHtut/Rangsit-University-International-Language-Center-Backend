from typing import Annotated
from fastapi import APIRouter, Depends
from src.database.model import Student
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import student_schema
from src.services.auth_services import auth_check, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/", response_model=list[student_schema.Student])
@auth_check("student:read")
def get_all_student(form_data: Annotated[OAuth2PasswordRequestForm, Depends(get_current_user)],db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students
