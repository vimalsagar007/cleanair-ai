import time
import asyncio
from typing import Dict, Any, Callable
from graph.state import PollutionState
from agents.location import LocationAgent
from agents.air_quality import AirQualityAgent
from agents.weather import WeatherAgent
from agents.trend import TrendAgent
from agents.health import HealthAgent
from agents.alert import AlertAgent
from agents.evidence import EvidenceAgent
from agents.final_response import FinalResponseAgent
from mcp.tools import PollutionMCPTools
from rag.retriever import RAGRetriever
from alert_engine.processor import AlertProcessor

class PollutionLangGraphWorkflow:
    """LangGraph Workflow Orchestrator for CLEANAIR AI."""

    def __init__(
        self,
        mcp_tools: PollutionMCPTools,
        rag_retriever: RAGRetriever,
        alert_processor: AlertProcessor
    ):
        self.location_agent = LocationAgent()
        self.aqi_agent = AirQualityAgent(mcp_tools)
        self.weather_agent = WeatherAgent(mcp_tools)
        self.trend_agent = TrendAgent(mcp_tools)
        self.health_agent = HealthAgent(rag_retriever)
        self.alert_agent = AlertAgent(alert_processor)
        self.evidence_agent = EvidenceAgent()

    def record_event(self, state: PollutionState, agent_name: str, task: str, tool_used: str, result_summary: str, latency_ms: float):
        state.agent_events.append({
            "agent": agent_name,
            "task": task,
            "tool": tool_used,
            "latency_ms": latency_ms,
            "result_summary": result_summary,
            "timestamp": time.strftime("%H:%M:%S")
        })

    async def location_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        res = await self.location_agent.resolve_location(state.user_query, state.location)
        state.location = res["city"]
        self.record_event(state, "LocationAgent", "Resolve location from query", "NLP Parser", f"Resolved city: {state.location}", round((time.time() - t0)*1000, 2))
        return state

    async def air_quality_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        aqi_data = await self.aqi_agent.fetch_air_quality(state.location, state.correlation_id)
        state.aqi = aqi_data.get("aqi")
        state.category = aqi_data.get("category")
        state.pollutants = aqi_data.get("pollutants", [])
        state.timestamp = aqi_data.get("timestamp", "")
        self.record_event(state, "AirQualityAgent", "Fetch current AQI & pollutants", "MCP get_current_aqi", f"AQI: {state.aqi} ({state.category})", round((time.time() - t0)*1000, 2))
        return state

    async def weather_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        wth = await self.weather_agent.fetch_weather(state.location, state.correlation_id)
        state.weather = wth
        self.record_event(state, "WeatherAgent", "Fetch weather conditions", "MCP get_weather", f"Temp: {wth.get('temperature_c')}C, Wind: {wth.get('wind_speed_kmh')} km/h", round((time.time() - t0)*1000, 2))
        return state

    async def pollution_analysis_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        tr = await self.trend_agent.analyze_trend(state.location, state.correlation_id)
        state.trend = tr
        self.record_event(state, "TrendAgent", "Analyze 24h pollution trend", "MCP get_pollution_trend", f"Trend: {tr.get('trend')}", round((time.time() - t0)*1000, 2))
        return state

    async def health_rag_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        contexts = await self.health_agent.retrieve_health_guidance(state.user_query, state.category or "Moderate")
        state.retrieved_documents = contexts
        self.record_event(state, "HealthAgent", "Retrieve RAG health guidelines", "RAG Retriever & FAISS Index", f"Retrieved {len(contexts)} PDF document contexts", round((time.time() - t0)*1000, 2))
        return state

    async def risk_analysis_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        aqi_val = state.aqi or 50
        if aqi_val <= 50:
            state.risk_level = "LOW"
        elif aqi_val <= 100:
            state.risk_level = "MODERATE"
        elif aqi_val <= 150:
            state.risk_level = "ELEVATED_SENSITIVE"
        elif aqi_val <= 200:
            state.risk_level = "HIGH"
        else:
            state.risk_level = "CRITICAL"
        self.record_event(state, "RiskAnalysisAgent", "Compute environmental risk category", "Risk Matrix Evaluator", f"Risk Level: {state.risk_level}", round((time.time() - t0)*1000, 2))
        return state

    async def alert_evaluation_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        pm25_val = next((p.get("value") for p in state.pollutants if p.get("pollutant") == "PM2.5"), 20.0)
        alert_res = await self.alert_agent.evaluate_alert(state.location, state.aqi or 50, float(pm25_val))
        state.alert_status = alert_res
        self.record_event(state, "AlertAgent", "Evaluate user threshold alert rules", "Alert Processor", f"Alert Triggered: {alert_res.get('alert_triggered')}", round((time.time() - t0)*1000, 2))
        return state

    async def grounding_validation_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        aqi_data = {"aqi": state.aqi, "category": state.category, "timestamp": state.timestamp, "location": state.location}
        draft_text = f"AQI is {state.aqi} in {state.location} ({state.category}). Recommended precautions available."
        g_res = await self.evidence_agent.validate_evidence(aqi_data, state.retrieved_documents, draft_text)
        state.grounding_result = g_res
        self.record_event(state, "EvidenceAgent", "Validate evidence & numerical grounding", "Grounding Validator", f"Grounding Valid: {g_res.get('is_valid')}", round((time.time() - t0)*1000, 2))
        return state

    async def retrieve_more_evidence(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        state.grounding_retry_count += 1
        more_contexts = await self.health_agent.retrieve_health_guidance(f"{state.user_query} detailed emergency safety", state.category or "Moderate")
        state.retrieved_documents.extend(more_contexts)
        self.record_event(state, "HealthAgent", "Retrieve fallback evidence (Retry loop)", "RAG Retriever Fallback", f"Retrieved {len(more_contexts)} extra contexts (Retry {state.grounding_retry_count})", round((time.time() - t0)*1000, 2))
        return state

    async def final_response_node(self, state: PollutionState) -> PollutionState:
        t0 = time.time()
        aqi_data = {
            "aqi": state.aqi,
            "category": state.category,
            "primary_pollutant": "PM2.5",
            "station_name": f"{state.location} Central Environmental Monitor",
            "timestamp": state.timestamp
        }
        res = FinalResponseAgent.assemble_response(
            query=state.user_query,
            city=state.location,
            aqi_data=aqi_data,
            weather_data=state.weather,
            trend_data=state.trend,
            health_contexts=state.retrieved_documents,
            alert_info=state.alert_status,
            grounding_result=state.grounding_result
        )
        state.final_response = res
        state.citations = res.get("citations", [])
        self.record_event(state, "FinalResponseAgent", "Assemble grounded response & citations", "Response Assembly Engine", "Generated final response with citations", round((time.time() - t0)*1000, 2))
        return state

    async def run(self, initial_state: PollutionState) -> PollutionState:
        state = initial_state
        state = await self.location_node(state)
        state = await self.air_quality_node(state)
        state = await self.weather_node(state)
        state = await self.pollution_analysis_node(state)
        
        # Parallel specialist nodes
        state = await self.health_rag_node(state)
        state = await self.risk_analysis_node(state)
        state = await self.alert_evaluation_node(state)
        
        # Grounding loop
        state = await self.grounding_validation_node(state)
        if not state.grounding_result.get("is_valid") and state.grounding_retry_count < state.max_grounding_retries:
            state = await self.retrieve_more_evidence(state)
            state = await self.grounding_validation_node(state)

        state = await self.final_response_node(state)
        return state

def build_pollution_graph(mcp_tools, rag_retriever, alert_processor):
    return PollutionLangGraphWorkflow(mcp_tools, rag_retriever, alert_processor)
