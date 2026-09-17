from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas


# ---------------------- Students ----------------------
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()


# ---------------------- Courses ----------------------
def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        title=course.title, description=course.description, capacity=course.capacity
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses(db: Session):
    return db.query(models.Course).all()


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def seats_taken(db: Session, course_id: int) -> int:
    return (
        db.query(func.count(models.Enrollment.id))
        .filter(models.Enrollment.course_id == course_id)
        .scalar()
        or 0
    )


def course_to_out(db: Session, course: models.Course) -> schemas.CourseOut:
    """Attach computed seat counts to a Course row for API responses."""
    taken = seats_taken(db, course.id)
    return schemas.CourseOut(
        id=course.id,
        title=course.title,
        description=course.description,
        capacity=course.capacity,
        seats_taken=taken,
        seats_available=course.capacity - taken,
    )


# ---------------------- Enrollments ----------------------
def get_enrollments(db: Session):
    return db.query(models.Enrollment).all()


def get_enrollment(db: Session, student_id: int, course_id: int):
    return (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.student_id == student_id,
            models.Enrollment.course_id == course_id,
        )
        .first()
    )


def get_student_enrollments(db: Session, student_id: int):
    return (
        db.query(models.Enrollment)
        .filter(models.Enrollment.student_id == student_id)
        .all()
    )


def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id, course_id=enrollment.course_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int) -> bool:
    db_enrollment = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.id == enrollment_id)
        .first()
    )
    if not db_enrollment:
        return False
    db.delete(db_enrollment)
    db.commit()
    return True
