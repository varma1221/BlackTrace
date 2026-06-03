"""
Database engine and base configuration for SQLAlchemy.

Establishes the core database connection using SQLAlchemy and defines the
declarative base used for all ORM model definitions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./blacktrace.db"

# Core SQLAlchemy engine responsible for managing database connections
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Factory for creating independent database sessions for request handling
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class inherited by all SQLAlchemy ORM database models
Base = declarative_base()
