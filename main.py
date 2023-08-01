from fastapi import FastAPI, Depends
from src.routes import (
    auth,
    peer,
    role,
    permission,
    user,
    mentor,
    student,
)
from src.database.setup import (
    Base,
    engine,
    get_db,
)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
# tempo
from src.schemas import *
from src.database.model import *
from src.services import auth_services

app = FastAPI()

# Path: src/routes/auth.py
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Path: src/routes/user.py
app.include_router(user.router, prefix="/user", tags=["User"])

# Path: src/routes/student.py
app.include_router(student.router, prefix="/student", tags=["Student"])

# Path: src/routes/mentor.py
app.include_router(mentor.router, prefix="/mentor", tags=["Mentor"])

# Path: src/routes/peer.py
app.include_router(peer.router, prefix="/peer", tags=["Peer"])

# Path: src/routes/role.py
app.include_router(role.router, prefix="/role", tags=["Role"])

# Path: src/routes/permission.py
app.include_router(permission.router, prefix="/permission",
                   tags=["Permission"])



@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root(db: Session = Depends(get_db)):

    fakeData(db=db)

    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

    

def fakeData(db: Session):
    user_read = Permission(
        route=Route.user,
        access=Access.read,
    )
    user_write = Permission(
        route=Route.user,
        access=Access.write,
    )
    user_full = Permission(
        route=Route.user,
        access=Access.full,
    )
    
    db.add_all([user_read, user_write, user_full,])
    db.commit()
    role1 = Role(
        name="admin",
        permissions=[user_read, user_write, user_full],
    )
    role2 = Role(
        name="mentor",
        permissions=[user_read, user_write],
    )
    role3 = Role(
        name="student",
        permissions=[user_read],
    )
    db.add_all([role1, role2, role3])
    db.commit()
    user1 = User(
        name="Sai",
        email="sai@potato.com",
        hashed_password=auth_services.pwd_context.hash("123"),
        role_id=role1.id,
    )
    user2 = User(
        name="Potato",
        email="potato@potato.com",
        hashed_password=auth_services.pwd_context.hash("123"),
        role_id=role2.id,
    )
    user3 = User(
        name="Nemo",
        email="nemo@potato.com",
        hashed_password=auth_services.pwd_context.hash("123"),
        role_id=role3.id,
    )
    db.add_all([user1, user2, user3])
    db.commit()


# Run Server
if __name__ == "__main__":
    import uvicorn
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
