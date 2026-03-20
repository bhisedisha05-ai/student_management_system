import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .routers import student_routes, subject_routes, seed_routes
from .database import engine, get_db, SessionLocal
from . import models, crud, schemas

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent



# Create database tables
models.Base.metadata.create_all(bind=engine)

# Seed initial data
def seed_initial_data():
    db = SessionLocal()
    try:
        subjects = crud.get_subjects(db)
        if not subjects:
            default_subjects = ["Maths", "Science", "English", "History", "Geography"]
            for subject_name in default_subjects:
                crud.create_subject(db, schemas.SubjectCreate(subject_name=subject_name))
    finally:
        db.close()

seed_initial_data()

# Initialize FastAPI app
app = FastAPI(title="Student Management System", version="1.0.0")

# Mount static files — uses relative path from this file
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Configure templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include routers
app.include_router(student_routes.router, prefix="/api")
app.include_router(subject_routes.router, prefix="/api")
app.include_router(seed_routes.router)          # already prefixed with /api/seed

# ── Frontend routes ──
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/students", response_class=HTMLResponse)
def students_page(request: Request, db: Session = Depends(get_db)):
    students = crud.get_students(db)
    return templates.TemplateResponse("students.html", {"request": request, "students": students})

@app.get("/add_student", response_class=HTMLResponse)
def add_student_page(request: Request, db: Session = Depends(get_db)):
    subjects = crud.get_subjects(db)
    return templates.TemplateResponse("add_student.html", {"request": request, "subjects": subjects})

@app.get("/edit_student/{student_id}", response_class=HTMLResponse)
def edit_student_page(request: Request, student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)
    return templates.TemplateResponse("edit_student.html", {"request": request, "student": student})

@app.get("/student_marks/{student_id}", response_class=HTMLResponse)
def student_marks_page(request: Request, student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)
    marks = crud.get_student_marks(db, student_id)
    subjects = crud.get_subjects(db)
    subject_dict = {subject.id: subject.subject_name for subject in subjects}

    # Convert to plain dicts so Jinja2 tojson can serialize them
    subjects_json = [{"id": s.id, "subject_name": s.subject_name} for s in subjects]
    marks_json    = [{"id": m.id, "student_id": m.student_id,
                      "subject_id": m.subject_id, "marks": m.marks} for m in marks]

    return templates.TemplateResponse(
        "student_marks.html",
        {
            "request":      request,
            "student":      student,
            "marks":        marks,
            "subjects":     subjects,
            "subject_dict": subject_dict,
            "subjects_json": subjects_json,   # ← serializable list
            "marks_json":    marks_json,       # ← serializable list
        }
    )

@app.get("/subjects", response_class=HTMLResponse)
def subjects_page(request: Request, db: Session = Depends(get_db)):
    subjects = crud.get_subjects(db)
    return templates.TemplateResponse("subjects.html", {"request": request, "subjects": subjects})

# ── API root ──
@app.get("/api")
def read_api_root():
    return {"message": "Welcome to Student Management System API"}