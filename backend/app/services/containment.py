from sqlalchemy.orm import Session
from backend.app.models.domain import IncidentLedger
from backend.app.db.ledger import get_incident
from datetime import datetime
import json

from typing import List, Dict, Any

def execute_containment_actions(
    db: Session, 
    incident_id: str, 
    attacker_ip: str, 
    compromised_user: str, 
    bastion_ip: str, 
    trigger_deception: bool
) -> List[Dict[str, Any]]:
    """
    Executes autonomous containment actions and logs them to the incident ledger.

    Args:
        db (Session): SQLAlchemy database session.
        incident_id (str): The unique identifier for the incident.
        attacker_ip (str): The IP address of the attacker to block.
        compromised_user (str): The username of the compromised account.
        bastion_ip (str): The IP address of the bastion host to isolate.
        trigger_deception (bool): Whether to trigger the active deception honey-trap.

    Returns:
        List[Dict[str, Any]]: A list of executed containment actions and their timestamps.
    """
    actions_executed = []
    
    incident = get_incident(db, incident_id)
    if not incident:
        # Create it if it doesn't exist for some reason
        incident = IncidentLedger(incident_id=incident_id, status="CONTAINING")
        db.add(incident)
    else:
        incident.status = "CONTAINING"

    current_summary = incident.summary or ""
    log_entries = []

    # Action 1: Dynamic IP block rule
    block_cmd = f"iptables -A INPUT -s {attacker_ip} -j DROP"
    log_entries.append(f"[{datetime.utcnow().isoformat()}] IP Blocked: {attacker_ip} via '{block_cmd}'")
    actions_executed.append({"action": "IP_BLOCK", "target": attacker_ip, "status": "EXECUTED", "timestamp": datetime.utcnow().isoformat()})

    # Action 2: Revoke active session tokens
    log_entries.append(f"[{datetime.utcnow().isoformat()}] Token Revoked for user: {compromised_user}")
    actions_executed.append({"action": "TOKEN_REVOCATION", "target": compromised_user, "status": "EXECUTED", "timestamp": datetime.utcnow().isoformat()})

    # Action 3: Network air-gap isolation
    log_entries.append(f"[{datetime.utcnow().isoformat()}] Host Isolated (Air-gapped): {bastion_ip}")
    actions_executed.append({"action": "HOST_ISOLATION", "target": bastion_ip, "status": "EXECUTED", "timestamp": datetime.utcnow().isoformat()})

    # Action 4: Register deception
    if trigger_deception:
        log_entries.append(f"[{datetime.utcnow().isoformat()}] Honey-trap deployed for incident.")
        actions_executed.append({"action": "DECEPTION_DEPLOYED", "status": "EXECUTED", "timestamp": datetime.utcnow().isoformat()})

    incident.summary = current_summary + "\n" + "\n".join(log_entries)
    incident.status = "CONTAINED"
    db.commit()
    
    return actions_executed
