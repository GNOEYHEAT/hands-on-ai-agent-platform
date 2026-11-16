"""문서 분석 및 보고서 작성 AI 에이전트 (L6: Model + Instruction)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent

from .mock_llm import MockLlm

load_dotenv(Path(__file__).resolve().parents[3] / ".env")    # 저장소 최상위 .env
MODEL_ID = os.getenv("DOC_AGENT_MODEL", "gemini-3.5-flash-lite")

# 실습: 아래 Instruction의 답변 형식이나 말투를 바꿔 보고 결과를 비교한다.
INSTRUCTION = """너는 문서 분석 및 보고서 작성 AI 에이전트다.
사용자가 붙여 넣은 문서를 읽고 다음 형식으로 한국어로 답한다.
## 요약 (3줄 이내)
## 핵심 항목 (글머리표)
## 문제점 (위험·지연·할 일)
## 보고서 (위 내용을 정리한 짧은 보고서)
문서에 없는 내용은 지어내지 않는다.
"""

root_agent = Agent(
    name="doc_report_agent",
    model=MockLlm() if MODEL_ID == "mock" else MODEL_ID,
    description="붙여 넣은 문서를 요약하고 보고서 형식으로 정리하는 에이전트",
    instruction=INSTRUCTION,
)
