from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.core.config import config
from src.agents.state import IncidentState
import os

def triage_agent(state: IncidentState) -> IncidentState:
    print(f"--- TRIAGE AGENT --- Correlation ID: {state['correlation_id']}")
    llm = ChatOpenAI(
        model=config.system.model, 
        temperature=config.system.temperature,
        api_key=os.getenv("OPENAI_API_KEY", "dummy_key")
    )
    
    prompt = PromptTemplate.from_template(
        "Analyze the following logs and categorize the failure into one of "
        "the following: Infrastructure, Code Bug, Test Flake, Dependency issue.\n\n"
        "Logs: {logs}\n\n"
        "Category:"
    )
    
    chain = prompt | llm
    
    # In a real environment with dummy keys, this would fail. We provide a fallback.
    if os.getenv("OPENAI_API_KEY", "dummy_key") == "dummy_key":
        category = "Code Bug - NullPointerException"
    else:
        response = chain.invoke({"logs": state["raw_logs"]})
        category = response.content.strip()

    return {"failure_category": category, "iteration": state.get("iteration", 0) + 1}
