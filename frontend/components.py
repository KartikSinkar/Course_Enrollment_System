"""
All the actual Streamlit widgets (st.header, st.button, st.form, etc.) live
here as small reusable functions. app.py just calls these — it doesn't build
any UI elements itself.
"""

import streamlit as st
import api_client


# ---------------------- Page header ----------------------
def render_page_header():
    st.set_page_config(page_title="Course Enrollment System", page_icon="🎓", layout="wide")
    st.title("🎓 Course Enrollment System")
    st.caption("Frontend for the FastAPI Course Enrollment backend — make sure the API is running on port 8000.")


def render_api_down_warning():
    st.error("⚠️ Can't reach the API. Run `uvicorn main:app --reload` inside the backend folder first.")


# ---------------------- Courses ----------------------
def render_add_course_form():
    st.subheader("Add a new course")
    with st.form("add_course_form", clear_on_submit=True):
        title = st.text_input("Course title")
        description = st.text_area("Description", height=80)
        capacity = st.number_input("Capacity (seats)", min_value=1, step=1, value=10)
        submitted = st.form_submit_button("Create course")

        if submitted:
            if not title:
                st.warning("Please enter a course title.")
            else:
                resp = api_client.create_course(title, description, int(capacity))
                if resp.status_code == 201:
                    st.success(f"Course '{title}' created!")
                else:
                    st.error(resp.json().get("detail", "Something went wrong."))


def render_course_list(courses: list):
    st.subheader("All courses")
    if not courses:
        st.info("No courses yet. Add one above.")
        return

    for c in courses:
        full = c["seats_available"] <= 0
        badge = "🔴 FULL" if full else f"🟢 {c['seats_available']} seat(s) left"
        with st.container(border=True):
            st.markdown(f"**#{c['id']} — {c['title']}**  {badge}")
            if c.get("description"):
                st.caption(c["description"])
            st.caption(f"Capacity: {c['capacity']} | Enrolled: {c['seats_taken']}")


# ---------------------- Students ----------------------
def render_add_student_form():
    st.subheader("Add a new student")
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add student")

        if submitted:
            if not name or not email:
                st.warning("Please fill in both fields.")
            else:
                resp = api_client.create_student(name, email)
                if resp.status_code == 201:
                    st.success(f"Student '{name}' added!")
                else:
                    st.error(resp.json().get("detail", "Something went wrong."))


def render_student_list(students: list):
    st.subheader("All students")
    if not students:
        st.info("No students yet. Add one above.")
        return

    for s in students:
        st.write(f"**#{s['id']}** — {s['name']} ({s['email']})")


# ---------------------- Enrollments ----------------------
def render_enroll_form(students: list, courses: list):
    st.subheader("Enroll a student in a course")

    if not students:
        st.info("Add a student first (see the Students tab).")
        return
    if not courses:
        st.info("Add a course first (see the Courses tab).")
        return

    student_map = {f"{s['name']} ({s['email']})": s["id"] for s in students}
    course_map = {
        f"{c['title']} — {c['seats_available']} seat(s) left": c["id"] for c in courses
    }

    student_choice = st.selectbox("Student", list(student_map.keys()))
    course_choice = st.selectbox("Course", list(course_map.keys()))

    if st.button("Enroll"):
        resp = api_client.create_enrollment(student_map[student_choice], course_map[course_choice])
        if resp.status_code == 201:
            st.success("Enrolled successfully! 🎉")
            st.rerun()
        else:
            st.error(resp.json().get("detail", "Something went wrong."))


def render_enrollment_list(enrollments: list):
    st.subheader("All enrollments")
    if not enrollments:
        st.info("No enrollments yet.")
        return

    for e in enrollments:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(
                f"**#{e['id']}** — {e['student']['name']} → {e['course']['title']} "
                f"(enrolled at {e['enrolled_at'][:19].replace('T', ' ')})"
            )
        with col2:
            if st.button("Cancel", key=f"cancel_{e['id']}"):
                del_resp = api_client.cancel_enrollment(e["id"])
                if del_resp.status_code == 204:
                    st.success("Cancelled.")
                    st.rerun()
                else:
                    st.error("Could not cancel.")
