from pydantic import BaseModel
from datetime import date
from typing import Optional

# Student schemas
class StudentBase(BaseModel):
    name: str
    roll_number: int
    standard: int
    division: str
    dob: date

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    roll_number: Optional[int] = None
    standard: Optional[int] = None
    division: Optional[str] = None
    dob: Optional[date] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

# Subject schemas
class SubjectBase(BaseModel):
    subject_name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True

# Marks schemas
class MarksBase(BaseModel):
    student_id: int
    subject_id: int
    marks: int

class MarksCreate(MarksBase):
    pass

class MarksResponse(MarksBase):
    id: int

    class Config:
        from_attributes = True