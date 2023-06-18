from fastapi import APIRouter, Depends
from src.database.model import Mentor
from src.database.setup import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/create")
def create_mentor(db: Session = Depends(get_db)):
    pass

