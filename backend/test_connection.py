"""
Run this file directly to check that your PostgreSQL connection works,
BEFORE running the actual FastAPI app.

Usage:
    python test_connection.py
"""

from sqlalchemy import text
from database import engine, SQLALCHEMY_DATABASE_URL


def test_connection():
    print(f"Attempting to connect to: {SQLALCHEMY_DATABASE_URL}")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print("✅ Connection successful!")
            print(f"PostgreSQL version: {version}")
    except Exception as e:
        print("❌ Connection failed.")
        print(f"Error: {e}")
        print(
            "\nCommon fixes:\n"
            "  1. Is PostgreSQL actually running? (check pgAdmin or the postgresql service)\n"
            "  2. Does the database exist? Run: CREATE DATABASE course_enrollment_db;\n"
            "  3. Is your .env file correct? Compare it against .env.example\n"
            "  4. Is the username/password in DATABASE_URL correct?\n"
            "  5. Is the port 5432 correct and not blocked by a firewall?"
        )


if __name__ == "__main__":
    test_connection()
