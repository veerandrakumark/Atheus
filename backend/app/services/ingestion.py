from backend.app.models.schemas import TelemetryEvent, AnomalyAlert
from backend.app.services.baseline_scorer import scorer
from typing import List

async def process_telemetry_batch(events: List[TelemetryEvent]) -> List[AnomalyAlert]:
    """
    Ingests a batch of telemetry events and passes them through the async baseline scorer.
    """
    alerts = []
    for event in events:
        alert = await scorer.score_event(event)
        if alert:
            alerts.append(alert)
    return alerts
