# Model Context Protocol (MCP) Design

The dedicated Pollution MCP Server (`mcp/`) exposes 14 enterprise tools:

1. `get_current_aqi`
2. `get_pollutants`
3. `get_aqi_history`
4. `get_pollution_trend`
5. `get_weather`
6. `get_forecast`
7. `get_monitoring_stations`
8. `get_nearby_monitoring_stations`
9. `get_location_information`
10. `get_pollution_sources`
11. `get_user_alert_preferences`
12. `save_alert_preference`
13. `create_alert`
14. `get_active_alerts`

## Enterprise Capabilities
* **Pydantic Schemas**: Strict type checking and validation on inputs and outputs.
* **Authentication & Authorization**: Internal bearer token validation.
* **Resilience**: Configurable execution timeouts, exponential backoff retries, and structured error responses.
* **Correlation Tracking**: Every MCP call receives a unique `correlation_id` passed through the agent workflow for observability.
