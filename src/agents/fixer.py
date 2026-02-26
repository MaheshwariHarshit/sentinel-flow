from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.core.config import config
from src.agents.state import IncidentState
import os

def fixer_agent(state: IncidentState) -> IncidentState:
    print(f"--- FIXER AGENT ---")
    
    if os.getenv("OPENAI_API_KEY", "dummy_key") == "dummy_key":
        fix = "Add null check: if (name == null) { return; }"
        rca = f"Root Cause Analysis:\nCategory: {state.get('failure_category')}\nAnalysis: {state.get('debug_analysis')}\nFix: {fix}"
        return {"suggested_fix": fix, "rca_report": rca}

    llm = ChatOpenAI(
        model=config.system.model, 
        temperature=config.system.temperature,
        api_key=os.getenv("OPENAI_API_KEY", "dummy_key")
    )
    
    prompt = PromptTemplate.from_template(
        "Generate a fix and a Root Cause Analysis (RCA) report based on this debug analysis.\n\n"
        "Debug Analysis: {analysis}\n\n"
        "Historical Context: {history}\n\n"
        "Format your answer as:\n"
        "FIX:\n<your fix here>\n\n"
        "RCA:\n<rca report here>"
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "analysis": state.get("debug_analysis", ""),
        "history": str(state.get("historical_context", []))
    })
    
    content = response.content
    fix_part = content.split("RCA:")[0].replace("FIX:", "").strip()
    rca_part = content.split("RCA:")[-1].strip() if "RCA:" in content else content
    
    return {"suggested_fix": fix_part, "rca_report": rca_part}
