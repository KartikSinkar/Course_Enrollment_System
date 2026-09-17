"""
Every function here talks to the FastAPI backend over HTTP.
Keeping all requests.get/post/delete calls in one place means components.py
and app.py never need to know the API's URLs or JSON shapes directly.
"""

import requests

API_URL = "http://127.0.0.1:8000"


# ---------------------- Students ----------------------
def get_students():
    resp = requests.get(f"{API_URL}/students")
    resp.raise_for_status()
    return resp.json()


def create_student(name: str, email: str):
    resp = requests.post(f"{API_URL}/students", json={"name": name, "email": email})
    return resp


# ---------------------- Courses ----------------------
def get_courses():
    resp = requests.get(f"{API_URL}/courses")
    resp.raise_for_status()
    return resp.json()


def create_course(title: str, description: str, capacity: int):
    resp = requests.post(
        f"{API_URL}/courses",
        json={"title": title, "description": description, "capacity": capacity},
    )
    return resp


# ---------------------- Enrollments ----------------------
def get_enrollments():
    resp = requests.get(f"{API_URL}/enrollments")
    resp.raise_for_status()
    return resp.json()


def create_enrollment(student_id: int, course_id: int):
    resp = requests.post(
        f"{API_URL}/enrollments",
        json={"student_id": student_id, "course_id": course_id},
    )
    return resp


def cancel_enrollment(enrollment_id: int):
    resp = requests.delete(f"{API_URL}/enrollments/{enrollment_id}")
    return resp


def is_api_reachable() -> bool:
    """Quick health check so the UI can show a friendly message if the API is down."""
    try:
        requests.get(f"{API_URL}/", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False
