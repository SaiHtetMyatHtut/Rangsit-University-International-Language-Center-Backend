from sqlalchemy import Column, Integer, String
from src.database.setup import Base


class Student(Base):
    # Table Name
    __tablename__ = "students"

    # id name email hashed_password image_url role
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    role = Column(String, nullable=True)

    def repr(self):
        return f"Student(id={self.id}, name={self.name}, email={self.email}, hashed_password={self.hashed_password}, image_url={self.image_url}, role={self.role})"
