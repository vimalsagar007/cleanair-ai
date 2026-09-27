import asyncio
from a2a.router import A2ARouter
from a2a.contracts import A2ATaskMessage, A2ATaskType, A2AStatus

async def test_a2a_task_dispatch():
    router = A2ARouter()
    
    async def sample_handler(task: A2ATaskMessage):
        return {"processed_for": task.location}

    router.register_agent_handler("AirQualityAgent", sample_handler)

    task = A2ATaskMessage(
        task_type=A2ATaskType.POLLUTION_ANALYSIS,
        sender_agent="SupervisorAgent",
        target_agent="AirQualityAgent",
        location="Seattle",
        timestamp="",
        correlation_id="test_corr_1"
    )

    res = await router.dispatch_task(task)
    assert res.status == A2AStatus.COMPLETED
    assert res.result_data["processed_for"] == "Seattle"
