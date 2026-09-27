import uuid
import time
from typing import Dict, Any, Optional, List
from models.alert_models import AlertConfig, AlertEvent, AlertSeverity
from alert_engine.pubsub_mock import PubSubTopicEmulator
from alert_engine.notifier import NotificationService

class AlertProcessor:
    """Configurable alert engine evaluating measurements against user thresholds."""

    def __init__(self, pubsub: PubSubTopicEmulator, notifier: NotificationService):
        self.pubsub = pubsub
        self.notifier = notifier
        self.user_configs: Dict[str, AlertConfig] = {
            "default_user": AlertConfig(
                user_id="default_user",
                config_id="cfg_default",
                city="San Francisco",
                aqi_threshold=100,
                pm25_threshold=35.4,
                notify_rapid_deterioration=True,
                channels=["in_app", "email"],
                is_active=True
            )
        }

    def register_config(self, config: AlertConfig):
        self.user_configs[config.user_id] = config

    async def evaluate_measurement(self, city: str, current_aqi: int, pm25_val: float) -> Optional[AlertEvent]:
        # Find active user config for this city
        target_config = None
        for cfg in self.user_configs.values():
            if cfg.is_active and cfg.city.lower() == city.lower():
                target_config = cfg
                break

        if not target_config:
            # Fallback default threshold check (AQI > 100)
            if current_aqi > 100:
                target_config = AlertConfig(
                    user_id="anonymous",
                    config_id="cfg_anon",
                    city=city,
                    aqi_threshold=100,
                    pm25_threshold=35.4
                )
            else:
                return None

        # Check threshold
        if current_aqi >= target_config.aqi_threshold:
            severity = AlertSeverity.WARNING if current_aqi < 150 else (AlertSeverity.HIGH if current_aqi < 200 else AlertSeverity.CRITICAL)
            event = AlertEvent(
                alert_id=f"alt_{uuid.uuid4().hex[:8]}",
                config_id=target_config.config_id,
                user_id=target_config.user_id,
                city=city,
                station_id=f"stn_{city.lower()}_01",
                severity=severity,
                trigger_reason=f"AQI reached {current_aqi}, crossing configured threshold of {target_config.aqi_threshold}.",
                metric_name="AQI",
                measured_value=float(current_aqi),
                threshold_value=float(target_config.aqi_threshold),
                unit="AQI Points",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                recommended_action="Air quality alert: reduce prolonged outdoor activity and review health guidance.",
                dashboard_url=f"/#dashboard?city={city}"
            )

            # Publish event to Pub/Sub
            event_id = f"pub_evt_{event.alert_id}"
            await self.pubsub.publish("pollution-alerts", event.model_dump(), event_id=event_id)

            # Send multi-channel notification
            await self.notifier.send_notification(event, target_config.channels)
            return event

        return None
