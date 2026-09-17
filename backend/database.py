from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format: postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
# EDIT the username/password below to match your local PostgreSQL setup.
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:yourpassword@localhost:5432/yourdatabasename"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a DB session per request and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
