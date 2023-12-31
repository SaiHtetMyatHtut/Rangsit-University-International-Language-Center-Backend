from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.schemas import peer_schema
from src.database.model import Peer, User, Route, Access
from src.services.auth_services import auth_check
auth_scheme = HTTPBearer()

router = APIRouter()


@router.get("/", response_model=list[peer_schema.Peer])
def get_all_peer(db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    peers = db.query(Peer).all()
    return peers


@router.post("/select-mentor", response_model=peer_schema.Peer)
def select_mentor(peer_data: peer_schema.CreatePeer, db: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    student = db.query(User).filter(User.role_id == 3).filter(
        User.id == peer_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student not found",
        )
    mentor = db.query(User).filter(User.role_id == 2).filter(
        User.id == peer_data.mentor_id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mentor not found",
        )
    mentor_per_student = db.query(Peer).filter(
        Peer.mentor_id == peer_data.mentor_id).count()
    if mentor_per_student >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mentor already have 5 students",
        )
    peer = Peer(
        student_id=peer_data.student_id,
        mentor_id=peer_data.mentor_id,
        section_id=0,
        timestamp="some timestamp",
    )
    db.add(peer)
    db.commit()
    db.refresh(peer)

    return peer_schema.Peer(
        student_id=peer.student_id,
        mentor_id=peer.mentor_id,
        section_id=peer.section_id,
        timestamp=peer.timestamp,
    )


@router.delete("/mentor/{mentor_id}", response_model=list[peer_schema.Peer])
@auth_check(route=Route.user, access=Access.full)
async def delete_peer(mentor_id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    peers = db.query(Peer).filter(Peer.mentor_id == mentor_id).all()
    if not peers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Peer not found",
        )
    for i in peers:
         db.delete(i)
    db.commit()
   
    return peers

@router.delete("/student/{student_id}", response_model=peer_schema.Peer)
@auth_check(route=Route.user, access=Access.full)
async def remove_peer(student_id:int, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    peer = db.query(Peer).filter(Peer.student_id == student_id).first()
    if not peer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Peer not found",
        )
    db.delete(peer)
    db.commit()
    return peer