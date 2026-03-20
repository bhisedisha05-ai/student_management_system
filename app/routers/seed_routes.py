"""
seed_routes.py  —  Bulk fake-data seeder for Student Management System
Endpoints:
  POST /api/seed/students?count=N   → add N fake students
  POST /api/seed/marks?per_subject=N → add marks for every student × every subject
  DELETE /api/seed/reset             → wipe all marks + students (keeps subjects)
"""

import random
from datetime import date, timedelta

from faker import Faker
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(prefix="/api/seed", tags=["Seeder"])
fake = Faker("en_IN")           # Indian locale for realistic names

# ─── helpers ────────────────────────────────────────────────────────────────

DIVISIONS = ["A", "B", "C", "D"]

def _random_dob(standard: int) -> date:
    """Return a realistic DOB.  Standard 1 ≈ age 6, Standard 10 ≈ age 15."""
    base_age = 5 + standard          # std 1 → ~6 yrs, std 10 → ~15 yrs
    birth_year = date.today().year - base_age
    try:
        return date(birth_year, random.randint(1, 12), random.randint(1, 28))
    except ValueError:
        return date(birth_year, 6, 15)

def _marks_for_profile(profile: str) -> int:
    """Return a mark that fits the student's performance profile."""
    if profile == "topper":
        return random.randint(82, 100)
    elif profile == "average":
        return random.randint(50, 79)
    elif profile == "below_average":
        return random.randint(30, 49)
    else:                            # struggling
        return random.randint(5, 29)


# ─── POST /api/seed/students ─────────────────────────────────────────────────

@router.post("/students", summary="Bulk-add fake students")
def seed_students(
    count: int = Query(default=10, ge=1, le=500,
                       description="Number of fake students to create (1–500)"),
    db: Session = Depends(get_db),
):
    """
    Creates `count` fake students spread across Standards 1–10 and Divisions A–D.
    Each student gets a realistic Indian name, roll number, DOB, and standard/division.
    Roll numbers are unique **per standard+division batch**.
    """
    # Build a per-batch roll counter so roll numbers don't collide within a batch
    batch_roll_counter: dict[tuple, int] = {}

    created = []
    for _ in range(count):
        standard = random.randint(1, 10)
        division = random.choice(DIVISIONS)
        key = (standard, division)
        batch_roll_counter[key] = batch_roll_counter.get(key, 0) + 1

        # Offset so existing students don't clash (start from a high number)
        existing = (
            db.query(models.Student)
            .filter(
                models.Student.standard == standard,
                models.Student.division == division,
            )
            .count()
        )
        roll = existing + batch_roll_counter[key]

        student_in = schemas.StudentCreate(
            name=fake.name(),
            roll_number=roll,
            standard=standard,
            division=division,
            dob=_random_dob(standard),
        )
        db_student = crud.create_student(db, student_in)
        created.append(db_student.id)

    return {
        "message": f"✅ {len(created)} students added successfully.",
        "student_ids": created,
    }


# ─── POST /api/seed/marks ─────────────────────────────────────────────────────

@router.post("/marks", summary="Bulk-add marks for all students × all subjects")
def seed_marks(
    per_subject: int = Query(
        default=1, ge=1, le=1,
        description="Currently fixed at 1 mark entry per student per subject "
                    "(set per_subject=1).  Each student gets exactly 1 mark "
                    "per subject so the table stays clean.",
    ),
    overwrite: bool = Query(
        default=False,
        description="If True, delete existing marks before inserting new ones.",
    ),
    db: Session = Depends(get_db),
):
    """
    For **every student** in the DB, inserts one mark per subject.
    Students are randomly assigned a performance profile:
      • 25 % topper        (82–100)
      • 40 % average       (50–79)
      • 25 % below_average (30–49)
      • 10 % struggling    (5–29)

    The profile is fixed per student so marks are **internally consistent**
    across subjects (a topper won't randomly score 10 in one subject).
    """
    students = db.query(models.Student).all()
    subjects = db.query(models.Subject).all()

    if not students:
        raise HTTPException(status_code=400, detail="No students found. Seed students first.")
    if not subjects:
        raise HTTPException(status_code=400, detail="No subjects found. Check seed_initial_data().")

    if overwrite:
        db.query(models.Marks).delete()
        db.commit()

    profiles = ["topper", "average", "below_average", "struggling"]
    weights  = [0.25,      0.40,      0.25,             0.10]

    inserted = 0
    skipped  = 0

    for student in students:
        # Assign a stable profile for this student
        profile = random.choices(profiles, weights=weights, k=1)[0]

        for subject in subjects:
            # Skip if mark already exists for this student+subject combo
            existing = (
                db.query(models.Marks)
                .filter(
                    models.Marks.student_id == student.id,
                    models.Marks.subject_id == subject.id,
                )
                .first()
            )
            if existing and not overwrite:
                skipped += 1
                continue

            marks_in = schemas.MarksCreate(
                student_id=student.id,
                subject_id=subject.id,
                marks=_marks_for_profile(profile),
            )
            crud.create_marks(db, marks_in)
            inserted += 1

    return {
        "message": f"✅ Marks seeded successfully.",
        "students_processed": len(students),
        "subjects_per_student": len(subjects),
        "marks_inserted": inserted,
        "marks_skipped_already_exist": skipped,
    }


# ─── DELETE /api/seed/reset ───────────────────────────────────────────────────

@router.delete("/reset", summary="Wipe all students and marks (keeps subjects)")
def seed_reset(
    confirm: bool = Query(
        default=False,
        description="Must be True to actually delete data.",
    ),
    db: Session = Depends(get_db),
):
    """
    Deletes **all marks** and **all students**.  Subjects are preserved.
    Pass `?confirm=true` to execute; without it, returns a dry-run preview.
    """
    student_count = db.query(models.Student).count()
    marks_count   = db.query(models.Marks).count()

    if not confirm:
        return {
            "dry_run": True,
            "warning": "Pass ?confirm=true to actually delete data.",
            "would_delete": {
                "students": student_count,
                "marks": marks_count,
            },
        }

    db.query(models.Marks).delete()
    db.query(models.Student).delete()
    db.commit()

    return {
        "message": "🗑️ All students and marks deleted. Subjects preserved.",
        "deleted": {
            "students": student_count,
            "marks": marks_count,
        },
    }