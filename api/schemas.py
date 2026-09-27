from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or statement")
    location: Optional[str] = Field(default="San Francisco", description="City or location override")
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    correlation_id: str
    answer: str
    grounding_status: str
    location: str
    aqi: Optional[int]
    category: Optional[str]
    data_summary: Dict[str, Any]
    citations: List[Dict[str, Any]]
    agent_events: List[Dict[str, Any]]

class AlertCreateRequest(BaseModel):
    user_id: str = "default_user"
    city: str
    aqi_threshold: int = Field(default=100, ge=0, le=500)
    channels: List[str] = Field(default_factory=lambda: ["in_app", "email"])
