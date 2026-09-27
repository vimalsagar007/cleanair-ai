import asyncio
import logging
from typing import Dict, Any
from mcp.schemas import MCPToolRequest, MCPToolResponse
from mcp.tools import PollutionMCPTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PollutionMCPServer")

class PollutionMCPServer:
    """Standalone MCP Server implementation."""

    def __init__(self):
        self.tools = PollutionMCPTools()

    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        req = MCPToolRequest(**request_data)
        response: MCPToolResponse = await self.tools.execute_tool(req)
        return response.model_dump()

if __name__ == "__main__":
    server = PollutionMCPServer()
    logger.info("[MCP Server] Initialized standalone Pollution MCP Server.")
    
    # Test sample invocation
    async def main():
        res = await server.handle_request({
            "tool_name": "get_current_aqi",
            "arguments": {"city_or_lat": "San Francisco"}
        })
        print("MCP Server Sample Output:", res)

    asyncio.run(main())
