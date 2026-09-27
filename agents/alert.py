from typing import Dict, Any, Optional
from alert_engine.processor import AlertProcessor

class AlertAgent:
    """Agent responsible for checking AQI measurements against active alert policies."""

    def __init__(self, alert_processor: AlertProcessor):
        self.alert_processor = alert_processor

    async def evaluate_alert(self, city: str, current_aqi: int, pm25_val: float) -> Dict[str, Any]:
        alert_event = await self.alert_processor.evaluate_measurement(city, current_aqi, pm25_val)
        if alert_event:
            return {
                "alert_triggered": True,
                "event": alert_event.model_dump()
            }
        return {
            "alert_triggered": False,
            "message": "Current AQI is within configured user threshold limits."
        }
