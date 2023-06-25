from pydantic import BaseModel

class PeerBase(BaseModel):
    pass

class SelectMentor(BaseModel):
    mentor_id: int
    student_id: int
    section_id: int
    timestamp: str

    class Config:
        orm_mode = True