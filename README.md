# Course Enrollment System (FastAPI + Streamlit)

An ed-tech backend where students browse courses and enroll themselves.
Enrollment is blocked once a course hits capacity, and a student can't
enroll twice in the same course.

## Tables (3-table version)
- **students** — id, name, email
- **courses** — id, title, description, capacity
- **enrollments** — id, student_id (FK), course_id (FK), enrolled_at
  - unique constraint on (student_id, course_id) → no duplicate enrollment

Database: **PostgreSQL** (connected via SQLAlchemy + psycopg2).

## Folder structure
```
course_enrollment_system/         (project folder)
├── project_env/                  # your existing virtual environment
├── backend/
│   ├── database.py                # DB engine/session setup
│   ├── models.py                  # SQLAlchemy ORM tables
│   ├── schemas.py                 # Pydantic request/response models
│   ├── crud.py                    # Database read/write functions
│   ├── main.py                    # FastAPI app + all API endpoints
│   └── requirements.txt           # Backend dependencies
├── frontend/
│   ├── app.py                      # Main entry point (run this)
│   ├── components.py               # Streamlit UI pieces (forms, headers, lists)
│   ├── api_client.py               # All requests calls to the backend
│   └── requirements.txt            # Frontend dependencies
└── README.md
```

Drop the `backend/` and `frontend/` folders (and this README) straight into
the same project folder where `project_env/` already lives — they sit as
siblings, one level up from both.

## PostgreSQL setup (do this once, before running the backend)

1. **Install PostgreSQL** if you haven't already: https://www.postgresql.org/download/
   (Windows installer includes pgAdmin — a GUI for managing databases.)
2. **Create the database.** Open pgAdmin or `psql` and run:
   ```sql
   CREATE DATABASE course_enrollment_db;
   ```
3. **Set your connection string.** Open `backend/database.py` and edit this line
   to match your actual Postgres username/password:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:your_password@localhost:5432/course_enrollment_db"
   ```

## Setup (in VS Code terminal, from the project folder root)

```bash
# 1. Activate your existing virtual environment
project_env\Scripts\activate      # Windows
source project_env/bin/activate   # macOS/Linux

# 2. Install dependencies (both backend and frontend) into project_env
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

## Backend files
| File | Purpose |
|---|---|
| `database.py` | DB engine/session setup — edit the connection string here directly |
| `models.py` | SQLAlchemy ORM tables |
| `schemas.py` | Pydantic request/response models |
| `crud.py` | Database read/write functions |
| `main.py` | FastAPI app + all API endpoints |
| `test_connection.py` | Standalone script — run this FIRST to confirm Postgres connects properly |

## Test your PostgreSQL connection first

Before starting the API, confirm the database connection actually works:

```bash
cd backend
python test_connection.py
```

You should see `✅ Connection successful!` along with your Postgres version.
If it fails, the script prints the most common fixes (server not running,
database doesn't exist, wrong password, etc.).

## Run the API

```bash
cd backend
uvicorn main:app --reload
```

- API base URL: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- Tables are created automatically inside your `course_enrollment_db` Postgres database on first run.

## Frontend files
| File | Purpose |
|---|---|
| `app.py` | Main entry point — run this with Streamlit. Orchestrates the page/tabs. |
| `components.py` | All the actual Streamlit UI pieces (headers, forms, buttons, lists) |
| `api_client.py` | All `requests` calls to the FastAPI backend |

## Run the Streamlit frontend (in a second terminal, with project_env activated and API already running)

```bash
cd frontend
streamlit run app.py
```

## .gitignore reminder
Before pushing to GitHub, exclude the venv so the repo stays clean:
```
project_env/
__pycache__/
*.pyc
```

⚠️ **Important — password in code:** since your Postgres password is now
hardcoded directly in `backend/database.py`, and this repo is **public**,
change your Postgres password to something you don't mind being visible
(not one you reuse anywhere else), OR replace the real password with a
placeholder like `your_password` right before pushing, and only put the
real one back locally when running the app yourself.

Opens at http://localhost:8501 — lets you add students, add courses, enroll
students, view live seat counts, and cancel enrollments from a UI.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List all students |
| GET | `/students/{id}` | Get one student |
| POST | `/courses` | Create a course |
| GET | `/courses` | List all courses (with seats_taken / seats_available) |
| GET | `/courses/{id}` | Get one course |
| POST | `/enrollments` | Enroll a student in a course (validates capacity + duplicates) |
| GET | `/enrollments` | List all enrollments |
| GET | `/students/{id}/enrollments` | List a student's enrollments |
| DELETE | `/enrollments/{id}` | Cancel an enrollment (frees the seat) |

## Business rules implemented
- A course cannot accept more enrollments than its `capacity` → returns `409 Course is full`.
- A student cannot enroll twice in the same course → returns `400 already enrolled`.
- Cancelling an enrollment immediately frees the seat for someone else.
- Duplicate student emails are rejected.

## Suggested next steps (optional, for extra credit / polish)
- Add JWT auth so students can only cancel their *own* enrollments.
- Add a "waitlist" instead of a hard block when a course is full.
- Deploy the API (Render/Railway) so your LinkedIn demo can hit a live URL.
- Write a few Pytest tests using FastAPI's `TestClient`.

## Submission checklist
- [ ] Push this folder to a **public GitHub repo**
- [ ] Record a short demo (screen recording/screenshots) showing: creating a
      course with capacity, enrolling students up to the limit, a blocked
      enrollment once full, and a cancellation freeing a seat
- [ ] Post the demo on LinkedIn, tag the institute/instructor
- [ ] Submit the GitHub repo link + LinkedIn post link on the LMS
