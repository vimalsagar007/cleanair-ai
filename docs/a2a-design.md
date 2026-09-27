# Agent-to-Agent (A2A) Collaboration Protocol

The A2A framework (`a2a/`) enables structured task delegation between agents:

## Task Message Contract
```json
{
  "task_id": "task_a1b2c3d4",
  "task_type": "POLLUTION_ANALYSIS",
  "sender_agent": "SupervisorAgent",
  "target_agent": "AirQualityAgent",
  "location": "San Francisco",
  "timestamp": "2026-09-27T13:30:00Z",
  "correlation_id": "corr_xyz789",
  "timeout_seconds": 5.0,
  "retry_count": 0,
  "max_retries": 2
}
```

## Resilience Features
* **Timeouts & Circuit Breaking**: Automatically times out stale agent sub-tasks after 5.0 seconds.
* **Retries**: Implements exponential backoff retries (up to 2 retries per sub-task).
* **Audit Trail**: Every A2A task message sent and completed is recorded in the broker audit log.
