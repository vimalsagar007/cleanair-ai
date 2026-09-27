from typing import Dict, Any
from mcp.tools import PollutionMCPTools
from mcp.schemas import MCPToolRequest

class AirQualityAgent:
    """Agent responsible for querying measured air quality data via MCP."""

    def __init__(self, mcp_tools: PollutionMCPTools):
        self.mcp_tools = mcp_tools

    async def fetch_air_quality(self, city: str, correlation_id: str) -> Dict[str, Any]:
        req = MCPToolRequest(
            tool_name="get_current_aqi",
            arguments={"city_or_lat": city},
            correlation_id=correlation_id
        )
        resp = await self.mcp_tools.execute_tool(req)
        if resp.status == "SUCCESS" and resp.result:
            return resp.result
        return {}
