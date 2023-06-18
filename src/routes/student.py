from fastapi import APIRouter, Depends
from src.database.model import Student
from src.database.setup import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# @router.get("/", response_model=list[Student])
# def get_all_student(db: Session = Depends(get_db)):
#     students = db.query(Student).all()
#     return students
