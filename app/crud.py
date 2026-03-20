from sqlalchemy.orm import Session
from . import models, schemas

# ── Students ──
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    # Delete associated marks first
    db.query(models.Marks).filter(models.Marks.student_id == student_id).delete()
    db.delete(db_student)
    db.commit()
    return db_student

# ── Subjects ──
def get_subjects(db: Session):
    return db.query(models.Subject).all()

def get_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

# ── Marks ──
def get_student_marks(db: Session, student_id: int):
    return db.query(models.Marks).filter(models.Marks.student_id == student_id).all()

def get_marks_by_id(db: Session, marks_id: int):
    return db.query(models.Marks).filter(models.Marks.id == marks_id).first()

def create_marks(db: Session, marks: schemas.MarksCreate):
    db_marks = models.Marks(**marks.model_dump())
    db.add(db_marks)
    db.commit()
    db.refresh(db_marks)
    return db_marks

def update_marks(db: Session, marks_id: int, marks_update: schemas.MarksCreate):
    db_marks = get_marks_by_id(db, marks_id)
    if not db_marks:
        return None
    for key, value in marks_update.model_dump().items():
        setattr(db_marks, key, value)
    db.commit()
    db.refresh(db_marks)
    return db_marks

def delete_marks(db: Session, marks_id: int):
    db_marks = get_marks_by_id(db, marks_id)
    if not db_marks:
        return None
    db.delete(db_marks)
    db.commit()
    return db_marks