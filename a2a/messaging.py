import asyncio
from typing import Dict, Any, List
from .contracts import A2ATaskMessage, A2ATaskResult

class A2AMessageBroker:
    """In-memory broker for Agent-to-Agent message passing and audit logging."""

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def log_task_sent(self, task: A2ATaskMessage):
        self.audit_log.append({
            "event": "TASK_SENT",
            "task_id": task.task_id,
            "task_type": task.task_type.value,
            "sender": task.sender_agent,
            "target": task.target_agent,
            "location": task.location,
            "correlation_id": task.correlation_id,
            "timestamp": task.timestamp
        })

    def log_task_completed(self, result: A2ATaskResult):
        self.audit_log.append({
            "event": "TASK_COMPLETED",
            "task_id": result.task_id,
            "status": result.status.value,
            "responder": result.responder_agent,
            "latency_ms": result.execution_latency_ms,
            "correlation_id": result.correlation_id
        })

    def get_audit_trail(self, correlation_id: str) -> List[Dict[str, Any]]:
        return [entry for entry in self.audit_log if entry.get("correlation_id") == correlation_id]
