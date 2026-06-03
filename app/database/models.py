"""
SQLAlchemy ORM models for persistent storage.

Defines the database schema for security alerts and other core entities
within the BlackTrace ecosystem.
"""
from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base

class Alert(Base):
    """
    Persistence model for security alerts.

    Attributes:
        alert_id (int): Unique identifier for the alert record.
        threat_type (str): The classification of the detected security threat.
        source_ip (str): Originating IP address of the suspicious activity.
        severity (str): Calculated risk level (e.g., Critical, High, Medium, Low).
        status (str): Operational state of the alert (e.g., Active, Resolved).
        timestamp (datetime): UTC timestamp of the detection event.
        recommended_action (str): Suggested remediation steps for SOC analysts.
    """  
    __tablename__ = "alerts"
    
    alert_id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(String)
    source_ip = Column(String)
    severity = Column(String)
    status = Column(String)
    timestamp = Column(DateTime)
    recommended_action = Column(String)
