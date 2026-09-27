import uuid
import time
import logging
from typing import List, Dict, Any
from models.alert_models import AlertEvent, NotificationMessage

logger = logging.getLogger("NotifierService")

class NotificationService:
    """Multi-channel notification dispatcher (In-App, Email, Web Push)."""

    def __init__(self):
        self.delivered_notifications: List[NotificationMessage] = []

    async def send_notification(self, alert_event: AlertEvent, channels: List[str]) -> List[NotificationMessage]:
        sent = []
        for channel in channels:
            msg = NotificationMessage(
                notification_id=f"notif_{uuid.uuid4().hex[:8]}",
                user_id=alert_event.user_id,
                channel=channel,
                subject=f"Air Quality Alert for {alert_event.city}: AQI {int(alert_event.measured_value)}",
                body=f"Air-quality alert for your selected location ({alert_event.city}): AQI has reached {int(alert_event.measured_value)} (threshold: {int(alert_event.threshold_value)}). {alert_event.recommended_action}",
                alert_event_id=alert_event.alert_id,
                sent_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                status="DELIVERED"
            )
            self.delivered_notifications.append(msg)
            sent.append(msg)
            logger.info(f"[Notification Sent] Channel: {channel} | User: {msg.user_id} | Subject: {msg.subject}")
        return sent

    def get_user_notifications(self, user_id: str) -> List[NotificationMessage]:
        return [n for n in self.delivered_notifications if n.user_id == user_id or user_id == "all"]
