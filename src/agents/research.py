from src.agents.state import IncidentState
from src.services.pinecone_service import pinecone_service

def research_agent(state: IncidentState) -> IncidentState:
    print(f"--- RESEARCH AGENT ---")
    category = state.get("failure_category", "")
    query = f"Resolved incident for {category}"
    
    # Query pinecone
    matches = pinecone_service.query_similar_incidents(query, top_k=2)
    
    if not matches:
        historical_context = [{"title": "No past incidents found", "content": "N/A"}]
    else:
        historical_context = [
            {"title": match['metadata'].get('title', 'Unknown'), "content": match['metadata'].get('resolution', '')} 
            for match in matches
        ]
        
    return {"historical_context": historical_context}
