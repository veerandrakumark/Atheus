from sqlalchemy.orm import Session
from backend.app.models.domain import IncidentLedger, FeedbackLedger
import uuid

def create_incident(db: Session, incident_id: str, summary: str = ""):
    db_incident = IncidentLedger(
        incident_id=incident_id,
        status="DETECTED",
        summary=summary
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def update_incident_status(db: Session, incident_id: str, status: str):
    db_incident = db.query(IncidentLedger).filter(IncidentLedger.incident_id == incident_id).first()
    if db_incident:
        db_incident.status = status
        db.commit()
        db.refresh(db_incident)
    return db_incident

def create_feedback(db: Session, incident_id: str, feedback_type: str, notes: str = ""):
    db_feedback = FeedbackLedger(
        feedback_id=str(uuid.uuid4()),
        incident_id=incident_id,
        feedback_type=feedback_type,
        notes=notes
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_incident(db: Session, incident_id: str):
    return db.query(IncidentLedger).filter(IncidentLedger.incident_id == incident_id).first()
