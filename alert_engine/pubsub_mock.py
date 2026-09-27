import uuid
import time
import logging
from typing import Dict, Any, List, Callable, Awaitable

logger = logging.getLogger("PubSubEmulator")

class PubSubTopicEmulator:
    """In-memory Google Cloud Pub/Sub topic emulator with idempotency tracking."""

    def __init__(self):
        self.topics = ["pollution-updates", "pollution-alerts", "agent-events"]
        self.messages: Dict[str, List[Dict[str, Any]]] = {t: [] for t in self.topics}
        self.processed_event_ids: set = set()

    async def publish(self, topic: str, data: Dict[str, Any], event_id: str = None) -> str:
        if topic not in self.topics:
            raise ValueError(f"Unknown topic: {topic}")

        eid = event_id or f"evt_{uuid.uuid4().hex[:12]}"
        
        # Idempotency check: ignore duplicate event IDs
        if eid in self.processed_event_ids:
            logger.info(f"[PubSub] Event ID '{eid}' already processed (Idempotency skip).")
            return eid

        self.processed_event_ids.add(eid)
        msg_payload = {
            "event_id": eid,
            "topic": topic,
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data": data
        }
        self.messages[topic].append(msg_payload)
        logger.info(f"[PubSub Publish] Topic: {topic} | EventID: {eid}")
        return eid

    def get_topic_messages(self, topic: str) -> List[Dict[str, Any]]:
        return self.messages.get(topic, [])
