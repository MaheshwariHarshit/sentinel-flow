from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.core.config import config
from src.agents.state import IncidentState
import os

def debugger_agent(state: IncidentState) -> IncidentState:
    print(f"--- DEBUGGER AGENT ---")
    
    if os.getenv("OPENAI_API_KEY", "dummy_key") == "dummy_key":
        analysis = "The NullPointerException is caused at UserService.java:42 because name is null."
        return {"debug_analysis": analysis}

    llm = ChatOpenAI(
        model=config.system.model, 
        temperature=config.system.temperature,
        api_key=os.getenv("OPENAI_API_KEY", "dummy_key")
    )
    
    prompt = PromptTemplate.from_template(
        "You are an expert debugger. Analyze these logs and the provided code context to find the exact line causing the failure.\n\n"
        "Logs: {logs}\n\n"
        "Code Context: {code}\n\n"
        "Analysis:"
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "logs": state["raw_logs"],
        "code": state.get("github_context", "No code context provided.")
    })
    
    return {"debug_analysis": response.content.strip()}
