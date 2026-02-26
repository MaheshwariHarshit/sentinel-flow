from typing import TypedDict, List, Optional
import operator
from typing import Annotated

class IncidentState(TypedDict):
    correlation_id: str
    raw_logs: str
    github_context: str
    failure_category: Optional[str]
    historical_context: List[dict]
    debug_analysis: str
    suggested_fix: str
    rca_report: str
    iteration: int
