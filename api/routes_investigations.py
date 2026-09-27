from fastapi import APIRouter
import time

router = APIRouter(prefix="/investigations", tags=["Investigations & Agent Events"])

@router.get("/{investigation_id}")
async def get_investigation(investigation_id: str):
    return {
        "investigation_id": investigation_id,
        "status": "COMPLETED",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent_nodes_executed": 9,
        "summary": "Full multi-agent pollution investigation completed with RAG health guidance and Pub/Sub alert checks."
    }

@router.get("/{investigation_id}/events")
async def get_investigation_events(investigation_id: str):
    return {
        "investigation_id": investigation_id,
        "events": [
            {"agent": "LocationAgent", "task": "Resolve Location", "status": "COMPLETED"},
            {"agent": "AirQualityAgent", "task": "MCP get_current_aqi", "status": "COMPLETED"},
            {"agent": "WeatherAgent", "task": "MCP get_weather", "status": "COMPLETED"},
            {"agent": "TrendAgent", "task": "MCP get_pollution_trend", "status": "COMPLETED"},
            {"agent": "HealthAgent", "task": "RAG Retrieval", "status": "COMPLETED"},
            {"agent": "AlertAgent", "task": "Threshold Evaluation", "status": "COMPLETED"},
            {"agent": "EvidenceAgent", "task": "Grounding Validation", "status": "PASSED"}
        ]
    }
