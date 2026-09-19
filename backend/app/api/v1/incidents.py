from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.security import get_api_key
from backend.app.db.session import get_db
from backend.app.db.ledger import get_incident, create_incident, update_incident_status

router = APIRouter()

@router.get("/{incident_id}")
def read_incident(incident_id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    incident = get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.post("/")
def register_incident(incident_id: str, summary: str = "", db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return create_incident(db, incident_id, summary)
