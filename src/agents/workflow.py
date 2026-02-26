from langgraph.graph import StateGraph, START, END
from src.agents.state import IncidentState
from src.agents.triage import triage_agent
from src.agents.research import research_agent
from src.agents.debugger import debugger_agent
from src.agents.fixer import fixer_agent

def create_workflow() -> StateGraph:
    workflow = StateGraph(IncidentState)

    # Add Nodes
    workflow.add_node("triage", triage_agent)
    workflow.add_node("research", research_agent)
    workflow.add_node("debugger", debugger_agent)
    workflow.add_node("fixer", fixer_agent)

    # Add Edges
    workflow.add_edge(START, "triage")
    workflow.add_edge("triage", "research")
    workflow.add_edge("research", "debugger")
    workflow.add_edge("debugger", "fixer")
    workflow.add_edge("fixer", END)

    # Compile the graph
    app = workflow.compile()
    return app

incident_workflow = create_workflow()
