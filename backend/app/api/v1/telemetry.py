from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from backend.app.models.schemas import TelemetryEvent, AnomalyAlert
from backend.app.services.ingestion import process_telemetry_batch
from backend.app.services.correlation import correlator
from backend.app.core.security import get_api_key
import json
import os

router = APIRouter()

# Global state for simulation
SIMULATION_STATE = {
    "current_index": 0,
    "events": []
}

def load_events():
    if not SIMULATION_STATE["events"]:
        path = os.path.join(os.path.dirname(__file__), "../../data/telemetry_stream.json")
        with open(path, "r") as f:
            SIMULATION_STATE["events"] = json.load(f)

from backend.app.services.gemini_triage import enrich_dossier

@router.post("/simulate/step")
async def simulate_step(batch_size: int = 1, api_key: str = Depends(get_api_key)) -> Dict[str, Any]:
    """
    Emits the next batch of events from the simulated JSON telemetry stream.
    """
    load_events()
    start = SIMULATION_STATE["current_index"]
    end = start + batch_size
    batch_data = SIMULATION_STATE["events"][start:end]
    
    if not batch_data:
        return {"status": "done", "message": "No more events to simulate."}
    
    # Parse to models
    events = [TelemetryEvent(**e) for e in batch_data]
    
    # Process
    alerts = await process_telemetry_batch(events)
    dossiers = await correlator.correlate_alerts(alerts)
    
    # Enrich with AI
    enriched_dossiers = []
    for d in dossiers:
        ed = await enrich_dossier(d)
        enriched_dossiers.append(ed)
    
    SIMULATION_STATE["current_index"] = end
    
    return {
        "status": "success",
        "processed_events": len(events),
        "alerts_generated": len(alerts),
        "new_dossiers": len(enriched_dossiers),
        "dossiers": enriched_dossiers
    }

@router.post("/simulate/burst")
async def simulate_burst(api_key: str = Depends(get_api_key)) -> Dict[str, Any]:
    """
    Injects the full APT attack chain into the telemetry stream.
    """
    load_events()
    start = SIMULATION_STATE["current_index"]
    batch_data = SIMULATION_STATE["events"][start:]
    
    if not batch_data:
        return {"status": "done", "message": "No more events to simulate."}
        
    events = [TelemetryEvent(**e) for e in batch_data]
    
    # Process
    alerts = await process_telemetry_batch(events)
    dossiers = await correlator.correlate_alerts(alerts)
    
    # Enrich with AI
    enriched_dossiers = []
    for d in dossiers:
        ed = await enrich_dossier(d)
        enriched_dossiers.append(ed)
    
    SIMULATION_STATE["current_index"] = len(SIMULATION_STATE["events"])
    
    return {
        "status": "success",
        "processed_events": len(events),
        "alerts_generated": len(alerts),
        "new_dossiers": len(enriched_dossiers),
        "dossiers": enriched_dossiers
    }

@router.post("/simulate/reset")
async def simulate_reset(api_key: str = Depends(get_api_key)):
    """Resets the simulation index."""
    SIMULATION_STATE["current_index"] = 0
    correlator.active_incidents.clear()
    return {"status": "reset_successful"}
