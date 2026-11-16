"""문서 분석 및 보고서 작성 AI 에이전트 (L8: MCP 서버 + Function Tool)."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from .mock_llm import MockLlm
from .tools import analyze_document, save_report

load_dotenv(Path(__file__).resolve().parents[3] / ".env")    # 저장소 최상위 .env
MODEL_ID = os.getenv("DOC_AGENT_MODEL", "gemini-3.5-flash-lite")
MCP_SERVER = Path(__file__).resolve().parents[1] / "doc_mcp_server.py"

doc_mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(command=sys.executable, args=[str(MCP_SERVER)]),
        timeout=30,
    ),
    tool_filter=["list_documents", "read_document"],   # 필요한 도구만 연다(SEC-06)
)

INSTRUCTION = """너는 문서 분석 및 보고서 작성 AI 에이전트다.
1. 어떤 문서가 있는지 모르면 list_documents로 목록을 본다.
2. read_document로 문서를 읽는다(경로는 data/ 기준, 예: samples/meeting_notes.md).
3. analyze_document로 제목·핵심 항목·문제점을 뽑는다.
4. 요약, 핵심 항목, 문제점, 보고서 순서로 한국어로 답하고, save_report로 outputs/에 저장한다.
"""

root_agent = Agent(
    name="doc_report_agent",
    model=MockLlm() if MODEL_ID == "mock" else MODEL_ID,
    description="MCP 서버로 문서를 읽고 분석해 보고서를 작성하는 에이전트",
    instruction=INSTRUCTION,
    tools=[doc_mcp_tools, analyze_document, save_report],
)
