from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_number = Column(Integer, nullable=False)
    standard = Column(Integer, nullable=False)  # 1 to 10
    division = Column(String(10), nullable=False)  # A, B, C, etc.
    dob = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String(100), nullable=False, unique=True)

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    marks = Column(Integer, nullable=False)  # Assuming marks out of 100