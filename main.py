from fastapi import FastAPI
from src.routes import auth, student, mentor, peer
from src.database.setup import Base, engine
from fastapi.responses import HTMLResponse


app = FastAPI()

# Path: src/routes/auth.py
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Path: src/routes/student.py
app.include_router(student.router, prefix="/student", tags=["Student"])

# Path: src/routes/mentor.py
app.include_router(mentor.router, prefix="/mentor", tags=["Mentor"])

# Path: src/routes/peer.py
app.include_router(peer.router, prefix="/peer", tags=["Peer"])

# Check Server Status

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

# Run Server
if __name__ == "__main__":
    import uvicorn
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
