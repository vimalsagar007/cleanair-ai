from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AlertConfig(BaseModel):
    user_id: str
    config_id: str
    city: str
    aqi_threshold: int = Field(default=100, ge=0, le=500)
    pm25_threshold: Optional[float] = Field(default=35.4, ge=0)
    pm10_threshold: Optional[float] = Field(default=154.0, ge=0)
    notify_rapid_deterioration: bool = True
    notify_forecast_poor: bool = True
    channels: List[str] = Field(default_factory=lambda: ["in_app", "email"])
    is_active: bool = True

class AlertEvent(BaseModel):
    alert_id: str
    config_id: str
    user_id: str
    city: str
    station_id: str
    severity: AlertSeverity
    trigger_reason: str
    metric_name: str
    measured_value: float
    threshold_value: float
    unit: str
    timestamp: str
    recommended_action: str
    dashboard_url: str
    source: str = "CLEANAIR AI Alert Engine"
    acknowledged: bool = False

class NotificationMessage(BaseModel):
    notification_id: str
    user_id: str
    channel: str
    subject: str
    body: str
    alert_event_id: str
    sent_at: str
    status: str = "DELIVERED"
