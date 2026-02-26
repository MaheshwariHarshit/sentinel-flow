from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
import uuid

from src.agents.workflow import incident_workflow
from src.integrations.splunk import splunk_connector
from src.integrations.slack import slack_connector
from src.services.db import get_db, IncidentJob, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

class JenkinsWebhookPayload(BaseModel):
    job_name: str
    build_id: str
    status: str
    correlation_id: str # Used to fetch logs from Splunk

def process_incident_background(payload: JenkinsWebhookPayload):
    print(f"Starting background processing for correlation_id={payload.correlation_id}")
    db = SessionLocal()
    try:
        # 1. Fetch initial logs
        raw_logs = splunk_connector.fetch_logs(payload.correlation_id)
        
        # 2. Invoke LangGraph
        initial_state = {
            "correlation_id": payload.correlation_id,
            "raw_logs": raw_logs,
            "github_context": "",
            "failure_category": None,
            "historical_context": [],
            "debug_analysis": "",
            "suggested_fix": "",
            "rca_report": "",
            "iteration": 0
        }
        
        final_state = incident_workflow.invoke(initial_state)
        
        # 3. Save to DB
        incident = db.query(IncidentJob).filter(IncidentJob.correlation_id == payload.correlation_id).first()
        if incident:
            incident.status = "complete"
            incident.failure_type = final_state.get("failure_category")
            incident.rca_report = final_state.get("rca_report")
            incident.suggested_fix = final_state.get("suggested_fix")
            db.commit()
            
        # 4. Notify Slack
        slack_connector.send_situation_report(
            incident_id=payload.correlation_id,
            summary=final_state.get("failure_category", "Unknown Failure"),
            rca_preview=final_state.get("suggested_fix", "")
        )
        print(f"Finished processing correlation_id={payload.correlation_id}")
    finally:
        db.close()

@router.post("/webhook/jenkins")
async def handle_jenkins_webhook(
    payload: JenkinsWebhookPayload, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if payload.status != "FAILURE":
        return {"message": "Ignored - not a failure."}

    # Record in DB
    new_job = IncidentJob(
        correlation_id=payload.correlation_id,
        source="jenkins",
        status="triage"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # Spawn background task
    background_tasks.add_task(process_incident_background, payload)
    
    return {"message": "Incident processing started", "correlation_id": payload.correlation_id}
