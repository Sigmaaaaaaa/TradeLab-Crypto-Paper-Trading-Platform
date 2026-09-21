# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    # check_same_thread=False is required for SQLite with FastAPI.
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Recycle idle connections because hosted database connections can expire.
    engine_kwargs.update(pool_pre_ping=True, pool_recycle=1800)

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Use with FastAPI Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()