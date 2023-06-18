from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.database.setup import Base
from sqlalchemy.orm import relationship


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

class Mentor(Base):
    # Table Name
    __tablename__ = "mentors"

    # id name email hashed_password image_url role language ig_url fb_url line_url
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    role = Column(String, nullable=True)
    languages = Column(String, nullable=True)
    ig_url = Column(String, nullable=True)
    fb_url = Column(String, nullable=True)
    line_id = Column(String, nullable=True)

    def repr(self):
        return f"Mentor(id={self.id}, name={self.name}, email={self.email}, hashed_password={self.hashed_password}, image_url={self.image_url}, role={self.role}, language={self.language}, ig_url={self.ig_url}, fb_url={self.fb_url}, line_url={self.line_url})"
    
class Peer(Base):
    # Table Name
    __tablename__ = "peers"

    student_id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    timestamp = Column(String, nullable=False)

    sections = relationship("Section", back_populates="peers")

    def repr(self):
        return f"Peer(sid={self.sid}, mid={self.mid}, timestamp={self.timestamp})"
    

class Section(Base):
    # Table Name
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    peers = relationship("Peer", back_populates="sections")

    def repr(self):
        return f"Section(id={self.id}, name={self.name}, datetime={self.datetime})"

