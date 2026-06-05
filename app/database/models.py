"""
SQLAlchemy ORM models for persistent storage.

Defines the database schema for security alerts and other core entities
within the BlackTrace ecosystem.
"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
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

class SecurityEvent(Base):
    """
    Persistence model for raw ingested security events.

    Stores original telemetry before threat analysis and alert ingestion.
    Serves as the foundational event history layer for analytics,
    machine learning pipelines, and forensic investigations.

    Attributes:
        event_id (int): Unique identifier for the security event.
        source_ip (str): Originating IP address of the event source.
        event_type (str): Classification of the incoming security events.
        severity (str): Initial severity level associated with the event.
        message (str): Raw event description or telemetry payload.
        event_timestamp (datetime): Timestamp representing when the event originally occured.
        ingestion_timestamp (datetime): Timestamp representing when the event was received and persisted by BlackTrace.
    """

    __tablename__ = "security_events"

    event_id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    ingestion_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
