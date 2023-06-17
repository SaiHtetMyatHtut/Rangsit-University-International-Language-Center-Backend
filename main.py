from fastapi import FastAPI
from src.routes import auth
from src.database.setup import Base, engine

app = FastAPI()

# Path: src/routes/auth.py
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Check Server Status


@app.get("/")
async def root():
    return {"Server Status": "Online"}

# Run Server
if __name__ == "__main__":
    import uvicorn
    # temporary solution to drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # run server
    uvicorn.run(app, host="localhost", port=8000)
