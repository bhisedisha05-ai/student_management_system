from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/students", response_model=list[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id=student_id, student_update=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# Marks endpoints
@router.get("/marks/{student_id}", response_model=list[schemas.MarksResponse])
def read_student_marks(student_id: int, db: Session = Depends(get_db)):
    marks = crud.get_student_marks(db, student_id=student_id)
    return marks

@router.post("/marks", response_model=schemas.MarksResponse)
def create_marks(marks: schemas.MarksCreate, db: Session = Depends(get_db)):
    return crud.create_marks(db=db, marks=marks)

@router.put("/marks/{marks_id}", response_model=schemas.MarksResponse)
def update_marks(marks_id: int, marks: schemas.MarksCreate, db: Session = Depends(get_db)):
    db_marks = crud.update_marks(db, marks_id=marks_id, marks_update=marks)
    if db_marks is None:
        raise HTTPException(status_code=404, detail="Marks not found")
    return db_marks

@router.delete("/marks/{marks_id}")
def delete_marks(marks_id: int, db: Session = Depends(get_db)):
    db_marks = crud.delete_marks(db, marks_id=marks_id)
    if db_marks is None:
        raise HTTPException(status_code=404, detail="Marks not found")
    return {"message": "Marks deleted successfully"}