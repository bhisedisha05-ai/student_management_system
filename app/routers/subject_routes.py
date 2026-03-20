from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/subjects", response_model=list[schemas.SubjectResponse])
def read_subjects(db: Session = Depends(get_db)):
    subjects = crud.get_subjects(db)
    return subjects

@router.post("/subjects", response_model=schemas.SubjectResponse)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db=db, subject=subject)