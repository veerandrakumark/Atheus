import asyncio
import json
import os
from colorama import init, Fore, Style
from backend.app.db.session import engine
from backend.app.models.domain import Base
from backend.app.models.schemas import TelemetryEvent
from backend.app.services.ingestion import process_telemetry_batch
from backend.app.services.correlation import correlator
from backend.app.services.gemini_triage import enrich_dossier
from backend.app.services.deception import deploy_honey_trap
from backend.app.services.containment import execute_containment_actions
from backend.app.db.session import SessionLocal

init(autoreset=True)

async def run_simulation():
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    print(f"{Fore.CYAN}{Style.BRIGHT} ATHEUS E2E SIMULATION (HEADLESS MODE)")
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================\n")

    # 0. Initialize DB
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Ingest
    print(f"{Fore.YELLOW}[1/5] INGESTING TELEMETRY (20 events)")
    path = os.path.join("backend", "app", "data", "telemetry_stream.json")
    with open(path, "r") as f:
        events_data = json.load(f)
    events = [TelemetryEvent(**e) for e in events_data]
    await asyncio.sleep(0.5)

    # 2. Baseline
    print(f"{Fore.YELLOW}[2/5] BASELINE SCORER FILTER")
    alerts = await process_telemetry_batch(events)
    noise_filtered = len(events) - len(alerts)
    print(f"      Filtered {noise_filtered} noise events, {len(alerts)} anomalies flagged.")
    await asyncio.sleep(0.5)

    # 3. Correlation & Triage
    print(f"{Fore.YELLOW}[3/5] AI CORRELATION & TRIAGE")
    dossiers = await correlator.correlate_alerts(alerts)
    dossier = dossiers[0]
    # Call Gemini (with fallback expected if no key)
    dossier = await enrich_dossier(dossier)
    tactics = ", ".join(dossier.mitre_tactics) if dossier.mitre_tactics else "None"
    print(f"      Mapped Tactics: {tactics}")
    await asyncio.sleep(0.5)

    # 4. Deception
    print(f"{Fore.YELLOW}[4/5] ACTIVE DECEPTION TRIGGERED")
    trap = deploy_honey_trap("10.0.2.45")
    print(f"      {trap['decoy_type']} deployed at {trap['decoy_ip']}")
    await asyncio.sleep(0.5)

    # 5. Containment
    print(f"{Fore.YELLOW}[5/5] AUTONOMOUS CONTAINMENT")
    actions = execute_containment_actions(
        db=db,
        incident_id=dossier.incident_id,
        attacker_ip="198.51.100.23",
        compromised_user="svc_deployer",
        bastion_ip="10.0.1.10",
        trigger_deception=True
    )
    for act in actions:
        print(f"      - {act['action']}")
    await asyncio.sleep(0.5)

    # Verification
    from backend.app.db.ledger import get_incident
    incident_record = get_incident(db, dossier.incident_id)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}--> VERIFIED: Incident written to SQLite ledger with status: {incident_record.status} & DECEIVED.")
    db.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
