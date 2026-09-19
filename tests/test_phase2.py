import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.schemas import IncidentDossier
from backend.app.services.gemini_triage import enrich_dossier
from backend.app.db.session import get_db, engine
from backend.app.models.domain import Base

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup could go here

@pytest.mark.asyncio
async def test_triage_fallback():
    # Test that gemini triage falls back on timeout
    # We can simulate timeout by mocking or just passing a dossier and knowing no valid API key is present
    # Actually, we can just call it and since GEMINI_API_KEY is not set or invalid, it will throw an exception and fallback
    dummy_dossier = IncidentDossier(
        incident_id="INC-12345",
        status="DETECTED",
        alerts=[]
    )
    
    enriched = await enrich_dossier(dummy_dossier)
    
    # Since it falls back, it should read from incident_fallback.json
    assert enriched.threat_score == 92
    assert enriched.severity == "CRITICAL"
    assert "T1110 - Brute Force" in enriched.mitre_tactics
    assert enriched.incident_id == "INC-12345"  # ID was preserved

def test_containment_execution():
    headers = {"X-Atheus-Key": "dev-key-123"}
    payload = {
        "incident_id": "INC-TEST-001",
        "attacker_ip": "198.51.100.23",
        "compromised_user": "svc_deployer",
        "bastion_ip": "10.0.1.10",
        "trigger_deception": True,
        "target_ip": "10.0.2.45"
    }
    response = client.post("/api/v1/containment/execute", json=payload, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    actions = data["actions"]
    assert len(actions) == 4
    
    action_types = [a["action"] for a in actions]
    assert "IP_BLOCK" in action_types
    assert "DECEPTION_DEPLOYED" in action_types
    
    decoy = data["deception_status"]
    assert decoy is not None
    assert decoy["decoy_ip"] == "10.0.2.99"
    
def test_copilot_report():
    headers = {"X-Atheus-Key": "dev-key-123"}
    response = client.get("/api/v1/copilot/report?lens=executive", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "executive_report"
    assert "Zero customer data compromised" in data["business_impact"]

def test_copilot_chat_fallback():
    headers = {"X-Atheus-Key": "dev-key-123"}
    payload = {
        "incident_id": "INC-2026-APT-01",
        "query": "Why was host 10.0.1.10 isolated?"
    }
    response = client.post("/api/v1/copilot/chat", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "isolated" in data["reply"]
    assert "T1021" in data["cited_events"]
