from fastapi import APIRouter, Depends
from src.database.model import Mentor
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import mentor_schema
from passlib.context import CryptContext


router = APIRouter()

# create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_model=list[mentor_schema.Mentor])
def get_all_mentor(db: Session = Depends(get_db)):
    mentors = db.query(Mentor).all()
    return mentors

@router.post("/create", response_model=mentor_schema.Mentor)
def create_mentor(req_mentor: mentor_schema.MentorCreate ,db: Session = Depends(get_db)):
    mentor = Mentor(
        name=req_mentor.name,
        email=req_mentor.email,
        hashed_password=pwd_context.hash(req_mentor.password),
        image_url=req_mentor.image_url,
        role=req_mentor.role,
        languages=req_mentor.languages,
        ig_url=req_mentor.ig_url,
        fb_url=req_mentor.fb_url,
        line_id=req_mentor.line_id
    )
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor_schema.Mentor.from_orm(mentor)

