import uuid
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class A2ATaskType(str, Enum):
    POLLUTION_ANALYSIS = "POLLUTION_ANALYSIS"
    WEATHER_ANALYSIS = "WEATHER_ANALYSIS"
    HEALTH_GUIDANCE = "HEALTH_GUIDANCE"
    TREND_ANALYSIS = "TREND_ANALYSIS"
    ALERT_DECISION = "ALERT_DECISION"
    EVIDENCE_VERIFICATION = "EVIDENCE_VERIFICATION"

class A2AStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"

class A2ATaskMessage(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    task_type: A2ATaskType
    sender_agent: str
    target_agent: str
    location: str
    timestamp: str
    correlation_id: str
    context: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: float = 5.0
    retry_count: int = 0
    max_retries: int = 2

class A2ATaskResult(BaseModel):
    task_id: str
    task_type: A2ATaskType
    responder_agent: str
    status: A2AStatus
    result_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    correlation_id: str
    execution_latency_ms: float = 0.0
