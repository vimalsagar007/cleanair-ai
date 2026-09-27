from typing import Dict, Any, List
from a2a.router import A2ARouter
from a2a.contracts import A2ATaskMessage, A2ATaskType

class SupervisorAgent:
    """Supervisor Agent for query parsing, intent routing, and orchestrating A2A sub-tasks."""

    def __init__(self, a2a_router: A2ARouter):
        self.a2a_router = a2a_router

    async def orchestrate_investigation(self, user_query: str, city: str, correlation_id: str) -> Dict[str, Any]:
        # Delegate via A2A tasks
        pollution_task = A2ATaskMessage(
            task_type=A2ATaskType.POLLUTION_ANALYSIS,
            sender_agent="SupervisorAgent",
            target_agent="AirQualityAgent",
            location=city,
            timestamp="",
            correlation_id=correlation_id
        )
        pollution_res = await self.a2a_router.dispatch_task(pollution_task)

        weather_task = A2ATaskMessage(
            task_type=A2ATaskType.WEATHER_ANALYSIS,
            sender_agent="SupervisorAgent",
            target_agent="WeatherAgent",
            location=city,
            timestamp="",
            correlation_id=correlation_id
        )
        weather_res = await self.a2a_router.dispatch_task(weather_task)

        return {
            "city": city,
            "pollution_result": pollution_res.result_data if pollution_res.status == "COMPLETED" else {},
            "weather_result": weather_res.result_data if weather_res.status == "COMPLETED" else {}
        }
