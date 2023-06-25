from fastapi import FastAPI, Depends
from src.routes import auth, student, mentor, peer, role, permission
from src.database.setup import Base, engine, get_db
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
# tempo
from src.schemas import *
from src.database.model import Access, Role, Permission, Student, Mentor, Peer
from src.services.auth_services import pwd_context

app = FastAPI()

# Path: src/routes/auth.py
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Path: src/routes/student.py
app.include_router(student.router, prefix="/student", tags=["Student"])

# Path: src/routes/mentor.py
app.include_router(mentor.router, prefix="/mentor", tags=["Mentor"])

# Path: src/routes/peer.py
app.include_router(peer.router, prefix="/peer", tags=["Peer"])

# Path: src/routes/role.py
app.include_router(role.router, prefix="/role", tags=["Role"])

# Path: src/routes/permission.py
app.include_router(permission.router, prefix="/permission", tags=["Permission"])

# Check Server Status

@app.get("/", response_class=HTMLResponse)
async def root(db: Session = Depends(get_db)):
    role = Role(
        name="admin",
    )
    db.add(role)
    db.commit()
    # db.refresh(role)
    permission = Permission(
        route="student",
        access=Access.READ,
        role_id=role.id
    )
    db.add(permission)
    # db.refresh(permission)
    db.commit()
    permission2 = Permission(
        route="student",
        access=Access.WRITE,
        role_id=role.id
    )
    db.add(permission2)
    db.commit()
    # db.refresh(permission2)
    db.commit()
    user = Student(
        name="admin",
        email="sai@gmail.com",
        hashed_password = pwd_context.hash("123456"),
        # put random image in to image_url
        image_url="https://i.pravatar.cc/150?img=3",
        role_id=role.id
    )
    db.add(user)
    db.commit()
    # db.refresh(user)
    
    
    

    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

# Run Server
if __name__ == "__main__":
    import uvicorn
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
