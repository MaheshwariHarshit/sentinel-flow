import pytest
from src.agents.state import IncidentState
from src.agents.workflow import incident_workflow

def test_workflow_dry_run():
    # Dry test for LangGraph routing (it skips actual OpenAI calls because we set dummy APi keys logic)
    
    initial_state = {
        "correlation_id": "test-1234",
        "raw_logs": "Exception in thread main java.lang.NullPointerException",
        "github_context": "public void dummy() {}",
        "failure_category": None,
        "historical_context": [],
        "debug_analysis": "",
        "suggested_fix": "",
        "rca_report": "",
        "iteration": 0
    }
    
    # We invoke the graph
    print("Testing LangGraph Agentic Workflow")
    final_state = incident_workflow.invoke(initial_state)
    
    assert final_state["correlation_id"] == "test-1234"
    assert "NullPointerException" in final_state.get("failure_category", "")
    assert "debug_analysis" in final_state
    assert "suggested_fix" in final_state
    assert "rca_report" in final_state

    print(f"RCA Report generated:\n{final_state['rca_report']}")
