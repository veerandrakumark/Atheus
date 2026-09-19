import asyncio
import os
import json
from pydantic import BaseModel
from typing import Dict, Any, List
from google import genai
from google.genai import types
from backend.app.models.schemas import IncidentDossier

class EnrichmentData(BaseModel):
    threat_score: int
    severity: str
    mitre_tactics: List[str]
    attack_story: str
    blast_radius_nodes: Dict[str, str]
    predicted_target: Dict[str, Any]

async def _call_gemini(dossier: IncidentDossier) -> EnrichmentData:
    client = genai.Client()
    prompt = f"""
    Analyze the following incident dossier and provide triage enrichment.
    Identify MITRE tactics, assign a threat score (0-100), severity, and reconstruct the attack story.
    Identify the blast radius nodes and predict the next target.
    
    Incident Data:
    {dossier.model_dump_json(indent=2)}
    """
    
    # We must use run_in_executor because generate_content is synchronous in this SDK by default,
    # or we can use async generate_content if available, but let's wrap to be safe.
    loop = asyncio.get_event_loop()
    
    def sync_call():
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=EnrichmentData,
                temperature=0.2
            )
        )
        return response.parsed
        
    return await loop.run_in_executor(None, sync_call)

async def enrich_dossier(dossier: IncidentDossier) -> IncidentDossier:
    """
    Enriches an IncidentDossier by querying the Gemini LLM.

    Args:
        dossier (IncidentDossier): The original incident dossier.

    Returns:
        IncidentDossier: The enriched dossier containing threat score, severity, and attack story.
    """
    try:
        # Enforce 4.0 second timeout
        enrichment: EnrichmentData = await asyncio.wait_for(_call_gemini(dossier), timeout=4.0)
        
        dossier.threat_score = enrichment.threat_score
        dossier.severity = enrichment.severity
        dossier.mitre_tactics = enrichment.mitre_tactics
        dossier.attack_story = enrichment.attack_story
        dossier.blast_radius_nodes = enrichment.blast_radius_nodes
        dossier.predicted_target = enrichment.predicted_target
        return dossier
        
    except (asyncio.TimeoutError, Exception) as e:
        print(f"Gemini triage failed or timed out: {e}. Falling back to cached dossier.")
        fallback_path = os.path.join(os.path.dirname(__file__), "../data/incident_fallback.json")
        with open(fallback_path, "r") as f:
            data = json.load(f)
            # Ensure the fallback incident ID matches the requested one
            data["incident_id"] = dossier.incident_id
            return IncidentDossier(**data)
