from backend.app.models.schemas import TelemetryEvent, AnomalyAlert
import uuid

class BaselineScorer:
    def __init__(self):
        # In a real system, these thresholds would be loaded from a config or learned dynamically
        self.failed_auth_threshold = 5
        self.high_severity_threshold = 80
        self.unusual_ports = [445, 3389, 22] # E.g., SMB, RDP, SSH to unexpected targets

    async def score_event(self, event: TelemetryEvent) -> AnomalyAlert | None:
        """
        Async heuristic baseline scorer.
        Returns an AnomalyAlert if the event crosses thresholds, else None.
        """
        score = 0.0
        flags = []

        # 1. Action-based heuristics
        attempts = event.payload_meta.get("attempts", 0)
        if event.action == "failed_login":
            if attempts > self.failed_auth_threshold:
                score += 50.0
                flags.append("brute_force_auth")
            else:
                score += 20.0
                flags.append("authentication_failure")
        
        if event.action == "authorized_login" and not (event.source_ip.startswith("10.") or event.source_ip.startswith("192.168.")):
            score += 50.0
            flags.append("external_authorized_login")
        
        if event.action == "port_scan":
            score += 50.0
            flags.append("reconnaissance_behavior")

        if event.action == "data_exfiltration":
            score += 80.0
            flags.append("unusual_egress_volume")

        # 2. Severity baseline deviation
        if event.severity_baseline > self.high_severity_threshold:
            score += (event.severity_baseline - self.high_severity_threshold) * 1.5
            flags.append("high_severity_deviation")
        
        # 3. Payload inspection (mock)
        target_port = event.payload_meta.get("target_port")
        if target_port and target_port in self.unusual_ports:
            score += 30.0
            flags.append(f"unusual_target_port_{target_port}")
            
        bytes_out = event.payload_meta.get("bytes_out", 0)
        if bytes_out > 1000000000: # 1 GB
            score += 90.0
            flags.append("massive_data_transfer")

        if score >= 50.0:
            return AnomalyAlert(
                alert_id=str(uuid.uuid4()),
                event=event,
                heuristic_score=score,
                flagged_indicators=flags
            )
        return None

scorer = BaselineScorer()
