from typing import Dict, Any

def deploy_honey_trap(target_ip: str) -> Dict[str, Any]:
    """
    Simulates the deployment of a honey-token and fake database sandbox.
    When a threat moves laterally toward the target_ip, this spins up a decoy.
    """
    decoy_ip = "10.0.2.99"
    
    # In a real scenario, this would orchestrate infrastructure (e.g., K8s or AWS API)
    trap_details = {
        "decoy_ip": decoy_ip,
        "decoy_type": "Postgres-HoneyDB",
        "synthetic_credential_injected": "db_admin_backup",
        "status": "TRAP_ACTIVE",
        "diverted_traffic_bytes": 4820000000,
        "original_target_protected": target_ip
    }
    
    return trap_details
