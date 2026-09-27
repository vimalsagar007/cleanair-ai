import asyncio
from mcp.tools import PollutionMCPTools
from mcp.schemas import MCPToolRequest

async def test_mcp_get_current_aqi():
    tools = PollutionMCPTools()
    req = MCPToolRequest(tool_name="get_current_aqi", arguments={"city_or_lat": "San Francisco"})
    res = await tools.execute_tool(req)
    assert res.status == "SUCCESS"
    assert res.result["location"]["city"] == "San Francisco"
    assert "aqi" in res.result

async def test_mcp_invalid_tool():
    tools = PollutionMCPTools()
    req = MCPToolRequest(tool_name="non_existent_tool", arguments={})
    res = await tools.execute_tool(req)
    assert res.status == "ERROR"
    assert res.error.code == 404
