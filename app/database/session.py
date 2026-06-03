"""
Database session lifecycle management.

Provides dependency injection utilities for managing SQLAlchemy sessions
within FastAPI request cycles.
"""
from app.database.connection import SessionLocal

def get_db():
    """
    Generates a database session and ensures its cleanup.

    Yields:
        Session: A scoped SQLAlchemy database session for ORM operations.
    """
    db = SessionLocal() #Open Connection
    
    try:
        yield db #Request happens
        
    finally:
        db.close() #Close Connection
