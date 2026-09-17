from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
import crud
from database import engine, get_db

# Create tables on startup (SQLite file: course_enrollment.db)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Enrollment System",
    description=(
        "An ed-tech backend where students browse courses and enroll themselves. "
        "Enrollment is blocked once a course reaches capacity, and a student "
        "cannot enroll twice in the same course."
    ),
    version="1.0.0",
)


# ==================== Students ====================
@app.post(
    "/students",
    response_model=schemas.StudentOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student_by_email(db, student.email):
        raise HTTPException(status_code=400, detail="A student with this email already exists")
    return crud.create_student(db, student)


@app.get("/students", response_model=List[schemas.StudentOut], tags=["Students"])
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentOut, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ==================== Courses ====================
@app.post(
    "/courses",
    response_model=schemas.CourseOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    if course.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be greater than 0")
    db_course = crud.create_course(db, course)
    return crud.course_to_out(db, db_course)


@app.get("/courses", response_model=List[schemas.CourseOut], tags=["Courses"])
def list_courses(db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    return [crud.course_to_out(db, c) for c in courses]


@app.get("/courses/{course_id}", response_model=schemas.CourseOut, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.course_to_out(db, course)


# ==================== Enrollments ====================
@app.post(
    "/enrollments",
    response_model=schemas.EnrollmentOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    student = crud.get_student(db, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = crud.get_course(db, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if crud.get_enrollment(db, enrollment.student_id, enrollment.course_id):
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    taken = crud.seats_taken(db, course.id) # type: ignore
    if taken >= course.capacity: # type: ignore
        raise HTTPException(status_code=409, detail="Course is full — no seats available")

    try:
        return crud.create_enrollment(db, enrollment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")


@app.get("/enrollments", response_model=List[schemas.EnrollmentOut], tags=["Enrollments"])
def list_enrollments(db: Session = Depends(get_db)):
    return crud.get_enrollments(db)


@app.get(
    "/students/{student_id}/enrollments",
    response_model=List[schemas.EnrollmentOut],
    tags=["Enrollments"],
)
def list_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.get_student_enrollments(db, student_id)


@app.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Enrollments"])
def cancel_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    if not crud.delete_enrollment(db, enrollment_id):
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return None


@app.get("/", tags=["Root"])
def root():
    return {"message": "Course Enrollment System API is running. Visit /docs for interactive API docs."}
