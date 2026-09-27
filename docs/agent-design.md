# Multi-Agent Architecture & Design

CLEANAIR AI employs 9 specialized agent roles coordinated via LangGraph:

1. **Supervisor Agent**: Responsible for query intent detection, route planning, and A2A task dispatch.
2. **Location Agent**: Resolves user queries, IP/GPS input, or explicit city selections into standardized coordinates and station IDs.
3. **Air Quality Agent**: Interacts with the Pollution MCP server (`get_current_aqi`, `get_pollutants`) to fetch verified measurements.
4. **Weather Agent**: Fetches ambient temperature, humidity, wind vectors, and dispersion factors via MCP (`get_weather`).
5. **Pollution Trend Agent**: Evaluates 24-hour historical records (`get_pollution_trend`) to compute AQI deltas and trend direction.
6. **Health Guidance / RAG Agent**: Queries the FAISS-indexed RAG knowledge base for population-specific safety guidelines (children, elderly, outdoor workers, cardiac patients).
7. **Alert Agent**: Evaluates current measurements against user-defined alert threshold policies and triggers Pub/Sub alert events.
8. **Evidence & Grounding Agent**: Verifies numerical claims in draft outputs against raw tool measurements and citation coverage.
9. **Final Response Agent**: Synthesizes the clean final response with formatted footnote citations and execution trace metadata.
