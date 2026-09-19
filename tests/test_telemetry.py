from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_simulate_burst():
    # Since we have fallback for dev mode in security.py, no header is strictly required
    # However, let's include it for good measure.
    headers = {"X-Atheus-Key": "dev-key-123"}
    
    # Reset first
    res_reset = client.post("/api/v1/telemetry/simulate/reset", headers=headers)
    assert res_reset.status_code == 200
    
    # Burst
    response = client.post("/api/v1/telemetry/simulate/burst", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["processed_events"] == 20
    # Alerts should include the 4 APT stages plus maybe some noise
    assert data["alerts_generated"] >= 4
    
    # Dossiers should be generated
    assert data["new_dossiers"] >= 1
