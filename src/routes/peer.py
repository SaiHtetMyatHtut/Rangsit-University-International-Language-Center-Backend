from fastapi import APIRouter, Depends
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import peer_schema
from src.database.model import Peer

router = APIRouter()

@router.get("/")
def get_all_peer(db: Session = Depends(get_db)):
    peers = db.query(Peer).all()
    return peers

@router.post("/select-mentor")
def select_mentor(req_peer: peer_schema.SelectMentor,db: Session = Depends(get_db)):
    mentor_per_student = db.query(Peer).filter(Peer.mentor_id == req_peer.mentor_id).count()
    if mentor_per_student > 5:
        return {"message": "Mentor is full"}
    peer = Peer(
        student_id=req_peer.student_id,
        mentor_id=req_peer.mentor_id,
        section_id = 0,
        timestamp="some timestamp",
    )
    db.add(peer)
    db.commit()
    db.refresh(peer)

    peers = db.query(Peer).all()
    print(peers)
    return peers