from pydantic import BaseModel

class SelectMentor(BaseModel):
    mentor_id: int
    student_id: int