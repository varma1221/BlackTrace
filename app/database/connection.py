"""
Database engine and base configuration for SQLAlchemy.

Initializes the PostgreSQL database engine and provides the
session factory and declarative base used acorss the application
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Core SQLAlchemy engine responsible for managing PostgreSQL connections
engine = create_engine(DATABASE_URL)

# Factory for creating isolated database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class inherited by all ORM models
Base = declarative_base()
