"""L6 자동 검증: root_agent 구성 확인 + 모의 모델로 대화 한 번(키 불필요).

    python labs/03-adk-agent/check.py
"""
import asyncio
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
os.environ["DOC_AGENT_MODEL"] = "mock"  # .env보다 먼저 정해 모의 모델을 쓴다

from google.adk.agents import LlmAgent  # noqa: E402
from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from doc_report_agent.agent import root_agent  # noqa: E402


def fail(msg: str) -> None:
    sys.exit(f"FAIL: {msg}")


async def converse(message: str) -> str:
    runner = InMemoryRunner(agent=root_agent, app_name="check")
    session = await runner.session_service.create_session(app_name="check", user_id="student")
    text = ""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    async for event in runner.run_async(user_id="student", session_id=session.id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            text += "".join(p.text or "" for p in event.content.parts)
    return text


def main() -> None:
    if not isinstance(root_agent, LlmAgent) or root_agent.name != "doc_report_agent":
        fail("root_agent가 doc_report_agent라는 이름의 ADK Agent가 아닙니다")
    if not root_agent.instruction.strip():
        fail("instruction이 비어 있습니다")
    print(f"root_agent: {root_agent.name}, tools: {len(root_agent.tools)}개(이 실습은 도구 없음)")

    doc = (ROOT / "data" / "samples" / "meeting_notes.md").read_text(encoding="utf-8")
    text = asyncio.run(converse(doc))
    for heading in ("## 요약", "## 핵심 항목", "## 문제점", "## 보고서"):
        if heading not in text:
            fail(f"응답에 '{heading}'가 없습니다:\n{text}")
    print("응답 형식: 요약, 핵심 항목, 문제점, 보고서 확인(모의 모델)")
    print("CHECK OK")


if __name__ == "__main__":
    main()
