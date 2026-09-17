from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------------------- Student ----------------------
class StudentBase(BaseModel):
    name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------- Course ----------------------
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int


class CourseCreate(CourseBase):
    pass


class CourseOut(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats_taken: int
    seats_available: int


# ---------------------- Enrollment ----------------------
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    student: StudentOut
    course: CourseBase
