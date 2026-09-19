from backend.app.models.schemas import AnomalyAlert, IncidentDossier
import uuid

class CorrelationEngine:
    def __init__(self):
        self.active_incidents = {} # In-memory cache for simplicity

    async def correlate_alerts(self, alerts: list[AnomalyAlert]) -> list[IncidentDossier]:
        """
        Simple correlation engine grouping alerts by source IP.
        """
        new_dossiers = []
        for alert in alerts:
            source_ip = alert.event.source_ip
            if source_ip not in self.active_incidents:
                dossier = IncidentDossier(
                    incident_id=f"INC-{uuid.uuid4().hex[:8].upper()}",
                    status="DETECTED",
                    alerts=[alert]
                )
                self.active_incidents[source_ip] = dossier
                new_dossiers.append(dossier)
            else:
                self.active_incidents[source_ip].alerts.append(alert)
                
        return new_dossiers

correlator = CorrelationEngine()
