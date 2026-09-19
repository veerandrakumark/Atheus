from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any

from backend.app.core.security import get_api_key
from backend.app.db.session import get_db
from backend.app.services.containment import execute_containment_actions
from backend.app.services.deception import deploy_honey_trap

router = APIRouter()

class ContainmentRequest(BaseModel):
    incident_id: str
    attacker_ip: str
    compromised_user: str
    bastion_ip: str
    trigger_deception: bool = False
    target_ip: str = ""

@router.post("/execute")
def execute_containment(req: ContainmentRequest, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    # Deploy honey trap if requested
    deception_result = None
    if req.trigger_deception and req.target_ip:
        deception_result = deploy_honey_trap(req.target_ip)
        
    actions = execute_containment_actions(
        db=db,
        incident_id=req.incident_id,
        attacker_ip=req.attacker_ip,
        compromised_user=req.compromised_user,
        bastion_ip=req.bastion_ip,
        trigger_deception=req.trigger_deception
    )
    
    return {
        "status": "success",
        "actions": actions,
        "deception_status": deception_result
    }
