"""
Main frontend entry point.
Run with:  streamlit run app.py

This file just orchestrates the page: it fetches data via api_client and
hands it to components.py to render. It doesn't build any UI itself.
"""

import streamlit as st
import api_client
import components

components.render_page_header()

if not api_client.is_api_reachable():
    components.render_api_down_warning()
    st.stop()

tab_courses, tab_students, tab_enroll, tab_all_enroll = st.tabs(
    ["📚 Courses", "🧑‍🎓 Students", "✍️ Enroll", "📋 All Enrollments"]
)

# ---------------------- Courses tab ----------------------
with tab_courses:
    components.render_add_course_form()
    st.divider()
    courses = api_client.get_courses()
    components.render_course_list(courses)

# ---------------------- Students tab ----------------------
with tab_students:
    components.render_add_student_form()
    st.divider()
    students = api_client.get_students()
    components.render_student_list(students)

# ---------------------- Enroll tab ----------------------
with tab_enroll:
    students = api_client.get_students()
    courses = api_client.get_courses()
    components.render_enroll_form(students, courses)

# ---------------------- All Enrollments tab ----------------------
with tab_all_enroll:
    enrollments = api_client.get_enrollments()
    components.render_enrollment_list(enrollments)
