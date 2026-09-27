import time
import asyncio
import logging
from typing import Dict, Any, Callable, Awaitable, Optional
from .contracts import A2ATaskMessage, A2ATaskResult, A2AStatus, A2ATaskType
from .messaging import A2AMessageBroker

logger = logging.getLogger("A2ARouter")

class A2ARouter:
    """Inter-Agent Task Dispatcher supporting retries, timeouts, and audit logging."""

    def __init__(self, broker: Optional[A2AMessageBroker] = None):
        self.broker = broker or A2AMessageBroker()
        self.agent_handlers: Dict[str, Callable[[A2ATaskMessage], Awaitable[Dict[str, Any]]]] = {}

    def register_agent_handler(self, agent_name: str, handler: Callable[[A2ATaskMessage], Awaitable[Dict[str, Any]]]):
        self.agent_handlers[agent_name] = handler
        logger.info(f"[A2A Router] Registered handler for agent: '{agent_name}'")

    async def dispatch_task(self, task: A2ATaskMessage) -> A2ATaskResult:
        start_time = time.time()
        self.broker.log_task_sent(task)
        handler = self.agent_handlers.get(task.target_agent)

        if not handler:
            res = A2ATaskResult(
                task_id=task.task_id,
                task_type=task.task_type,
                responder_agent=task.target_agent,
                status=A2AStatus.FAILED,
                error_message=f"No agent handler registered for target agent: '{task.target_agent}'",
                correlation_id=task.correlation_id,
                execution_latency_ms=round((time.time() - start_time) * 1000, 2)
            )
            self.broker.log_task_completed(res)
            return res

        for attempt in range(task.max_retries + 1):
            try:
                task_res_data = await asyncio.wait_for(handler(task), timeout=task.timeout_seconds)
                res = A2ATaskResult(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    responder_agent=task.target_agent,
                    status=A2AStatus.COMPLETED,
                    result_data=task_res_data,
                    correlation_id=task.correlation_id,
                    execution_latency_ms=round((time.time() - start_time) * 1000, 2)
                )
                self.broker.log_task_completed(res)
                return res
            except asyncio.TimeoutError:
                logger.warning(f"[A2A Timeout] Task {task.task_id} target '{task.target_agent}' timed out (Attempt {attempt+1}/{task.max_retries+1})")
                if attempt == task.max_retries:
                    res = A2ATaskResult(
                        task_id=task.task_id,
                        task_type=task.task_type,
                        responder_agent=task.target_agent,
                        status=A2AStatus.TIMEOUT,
                        error_message=f"Agent '{task.target_agent}' timed out after {task.timeout_seconds}s.",
                        correlation_id=task.correlation_id,
                        execution_latency_ms=round((time.time() - start_time) * 1000, 2)
                    )
                    self.broker.log_task_completed(res)
                    return res
            except Exception as e:
                logger.error(f"[A2A Failure] Task {task.task_id} target '{task.target_agent}' failed: {str(e)}")
                if attempt == task.max_retries:
                    res = A2ATaskResult(
                        task_id=task.task_id,
                        task_type=task.task_type,
                        responder_agent=task.target_agent,
                        status=A2AStatus.FAILED,
                        error_message=str(e),
                        correlation_id=task.correlation_id,
                        execution_latency_ms=round((time.time() - start_time) * 1000, 2)
                    )
                    self.broker.log_task_completed(res)
                    return res
