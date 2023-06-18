from fastapi import APIRouter, Depends
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import peer_schema
from src.database.model import Peer

router = APIRouter()

@router.post("/select-mentor",response_model=list[peer_schema.SelectMentor])
def select_mentor(req_peer: peer_schema.SelectMentor,db: Session = Depends(get_db)):
    mentor_per_student = db.query(Peer).filter(Peer.mentor_id == req_peer.mentor_id).first()
    if mentor_per_student is not None:
        pass
    peer = Peer(
        student_id=req_peer.student_id,
        mentor_id=req_peer.mentor_id
    )
    db.add(peer)
    db.commit()
    db.refresh(peer)
    return peer_schema.SelectMentor.from_orm(peer)