from fastapi import FastAPI, Depends
from src.routes import auth
from src.database.setup import Base, engine

# Temporary Import
from fastapi import Depends
from src.database.setup import get_db
from sqlalchemy.orm import Session
from src.database.model import Student

app = FastAPI()

# Path: src/routes/auth.py
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Check Server Status
@app.get("/")
async def root(db: Session = Depends(get_db)):
    students = Student(name="John Doe", email="sai@gmail.com", hashed_password="123456")
    db.add(students)
    db.commit()
    db.refresh(students)

    student = db.query(Student).first()
    print(student.name)
    return {"Server Status": "Online"}

# Run Server
if __name__ == "__main__":
    import uvicorn
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="localhost", port=8000)