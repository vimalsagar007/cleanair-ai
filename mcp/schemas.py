import uuid
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field

class MCPToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    auth_token: Optional[str] = "bearer-mcp-internal-token"

class MCPError(BaseModel):
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None

class MCPToolResponse(BaseModel):
    tool_name: str
    status: str = "SUCCESS"  # SUCCESS or ERROR
    result: Optional[Dict[str, Any]] = None
    error: Optional[MCPError] = None
    correlation_id: str
    execution_time_ms: float = 0.0

class GetAQIInput(BaseModel):
    city_or_lat: str = Field(..., description="City name or latitude coordinate string")
    longitude: Optional[float] = None

class GetHistoryInput(BaseModel):
    city_or_lat: str
    hours: int = Field(default=24, ge=1, le=168)

class GetWeatherInput(BaseModel):
    city_or_lat: str

class AlertPrefInput(BaseModel):
    user_id: str
    city: str
    aqi_threshold: int = Field(default=100, ge=0, le=500)
    channels: List[str] = Field(default_factory=lambda: ["in_app"])
