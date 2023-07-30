from datetime import datetime
from pydantic import BaseModel

class PeerBase(BaseModel):
    pass

class Peer(PeerBase):
    mentor_id: int
    student_id: int
    section_id: int
    timestamp: str
    
    class Config:
        orm_mode = True
        
class CreatePeer(PeerBase):
    mentor_id: int
    student_id: int
    section_id: int
    timestamp: datetime = datetime.utcnow()

    class Config:
        orm_mode = True