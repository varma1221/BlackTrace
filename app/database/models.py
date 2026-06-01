"""
Database models for persisted BlackTrace records.

This module defines SQLAlchemy ORM models that map application data
to database tables.
"""
from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base

class Alert(Base):
    """
    Database model for a persisted security alert.

    Each Alert instance represents one row in the alerts table and stores
    the detection outcome needed for alert review and incident tracking.
    """    
    __tablename__ = "alerts"
    
    alert_id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(String)
    source_ip = Column(String)
    severity = Column(String)
    status = Column(String)
    timestamp = Column(DateTime)
    recommended_action = Column(String)
