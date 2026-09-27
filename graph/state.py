import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class PollutionState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_query: str = ""
    location: str = "San Francisco"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: str = ""
    aqi: Optional[int] = None
    category: Optional[str] = None
    pollutants: List[Dict[str, Any]] = Field(default_factory=list)
    weather: Dict[str, Any] = Field(default_factory=dict)
    historical_data: List[Dict[str, Any]] = Field(default_factory=list)
    trend: Dict[str, Any] = Field(default_factory=dict)
    retrieved_documents: List[Any] = Field(default_factory=list)
    health_guidance: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "LOW"
    alert_status: Dict[str, Any] = Field(default_factory=dict)
    grounding_result: Dict[str, Any] = Field(default_factory=dict)
    grounding_retry_count: int = 0
    max_grounding_retries: int = 2
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    agent_events: List[Dict[str, Any]] = Field(default_factory=list)
    final_response: Dict[str, Any] = Field(default_factory=dict)
