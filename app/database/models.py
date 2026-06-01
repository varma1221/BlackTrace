from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    alert_id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(String)
    source_ip = Column(String)
    severity = Column(String)
    status = Column(String)
    timestamp = Column(DateTime)
    recommended_action = Column(String)
