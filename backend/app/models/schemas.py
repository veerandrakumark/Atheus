from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TelemetryEvent(BaseModel):
    event_id: str
    timestamp: datetime
    source_type: str
    source_ip: str
    destination_ip: Optional[str] = None
    user: Optional[str] = None
    action: str
    severity_baseline: int
    payload_meta: Dict[str, Any] = Field(default_factory=dict)

class AnomalyAlert(BaseModel):
    alert_id: str
    event: TelemetryEvent
    heuristic_score: float
    flagged_indicators: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class IncidentDossier(BaseModel):
    incident_id: str
    status: str
    alerts: List[AnomalyAlert]
    threat_score: Optional[int] = None
    severity: Optional[str] = None
    mitre_tactics: List[str] = Field(default_factory=list)
    attack_story: Optional[str] = None
    blast_radius_nodes: Dict[str, str] = Field(default_factory=dict)
    predicted_target: Dict[str, Any] = Field(default_factory=dict)
    deception_status: str = "INACTIVE"
    decoy_details: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContainmentAction(BaseModel):
    action_id: str
    incident_id: str
    action_type: str
    status: str
    executed_at: datetime = Field(default_factory=datetime.utcnow)

class AnalystFeedback(BaseModel):
    feedback_id: str
    incident_id: str
    feedback_type: str # TRUE_POSITIVE, FALSE_POSITIVE, SEVERITY_OVERRIDE
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DecoyTrap(BaseModel):
    decoy_id: str
    type: str # e.g., HONEYTOKEN, FAKE_DB
    status: str # e.g., ACTIVE, TRIGGERED

class DeceptionState(BaseModel):
    decoy_id: str
    type: str
    target_lured: Optional[str] = None
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
