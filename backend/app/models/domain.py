from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class IncidentLedger(Base):
    __tablename__ = "incident_ledger"

    incident_id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True) # DETECTED, INVESTIGATING, CONTAINED, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    summary = Column(Text, nullable=True)

class FeedbackLedger(Base):
    __tablename__ = "feedback_ledger"

    feedback_id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, index=True)
    feedback_type = Column(String, index=True) # TRUE_POSITIVE, FALSE_POSITIVE, SEVERITY_OVERRIDE
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
