import asyncio
import os
from tests.test_mcp import test_mcp_get_current_aqi, test_mcp_invalid_tool
from tests.test_a2a import test_a2a_task_dispatch
from tests.test_rag import test_rag_retrieval
from tests.test_safety import test_prompt_injection_defense, test_grounding_validator
from tests.test_api import test_health_endpoint, test_air_quality_endpoint, test_chat_endpoint

async def run_all_tests():
    print("[Testing] Running MCP tests...")
    await test_mcp_get_current_aqi()
    await test_mcp_invalid_tool()

    print("[Testing] Running A2A tests...")
    await test_a2a_task_dispatch()

    print("[Testing] Running RAG tests...")
    test_rag_retrieval()

    print("[Testing] Running Safety tests...")
    test_prompt_injection_defense()
    test_grounding_validator()

    print("[Testing] Running API tests...")
    test_health_endpoint()
    test_air_quality_endpoint()
    test_chat_endpoint()

    print("\n✅ ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
