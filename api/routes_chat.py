from fastapi import APIRouter
from api.schemas import ChatRequest, ChatResponse
from graph.workflow import build_pollution_graph
from graph.state import PollutionState
from mcp.tools import PollutionMCPTools
from rag.retriever import RAGRetriever
from alert_engine.processor import AlertProcessor
from alert_engine.pubsub_mock import PubSubTopicEmulator
from alert_engine.notifier import NotificationService
from safety.injection_defense import PromptInjectionDefense

router = APIRouter(tags=["AI Chat"])

pubsub = PubSubTopicEmulator()
notifier = NotificationService()
alert_processor = AlertProcessor(pubsub, notifier)
mcp_tools = PollutionMCPTools()
rag_retriever = RAGRetriever()
workflow = build_pollution_graph(mcp_tools, rag_retriever, alert_processor)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Prompt injection check
    sanitized = PromptInjectionDefense.sanitize_input(request.message)
    user_q = sanitized["sanitized_text"]

    init_state = PollutionState(
        session_id=request.session_id or f"sess_{request.location.lower()}",
        user_query=user_q,
        location=request.location or "San Francisco"
    )

    final_state = await workflow.run(init_state)

    res = final_state.final_response
    return ChatResponse(
        session_id=final_state.session_id,
        correlation_id=final_state.correlation_id,
        answer=res.get("answer", "No response generated."),
        grounding_status=res.get("grounding_status", "UNKNOWN"),
        location=final_state.location,
        aqi=final_state.aqi,
        category=final_state.category,
        data_summary=res.get("data_summary", {}),
        citations=final_state.citations,
        agent_events=final_state.agent_events
    )
