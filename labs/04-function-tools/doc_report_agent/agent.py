"""문서 분석 및 보고서 작성 AI 에이전트 (L7: Function Tool 3개)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent

from .mock_llm import MockLlm
from .tools import analyze_document, read_document, save_report

load_dotenv(Path(__file__).resolve().parents[3] / ".env")    # 저장소 최상위 .env
MODEL_ID = os.getenv("DOC_AGENT_MODEL", "gemini-3.5-flash-lite")

INSTRUCTION = """너는 문서 분석 및 보고서 작성 AI 에이전트다.
1. 사용자가 data/ 안의 문서를 말하면 read_document로 읽는다. 내용을 붙여 넣었으면 바로 분석한다.
2. analyze_document로 제목·핵심 항목·문제점을 뽑는다.
3. 요약, 핵심 항목, 문제점, 보고서 순서로 한국어로 답한다.
4. 사용자가 원하거나 보고서를 만들었으면 save_report로 outputs/에 저장하고 경로를 알려 준다.
"""

root_agent = Agent(
    name="doc_report_agent",
    model=MockLlm() if MODEL_ID == "mock" else MODEL_ID,
    description="문서를 읽고 분석해 보고서를 작성하는 에이전트",
    instruction=INSTRUCTION,
    tools=[read_document, analyze_document, save_report],
)
