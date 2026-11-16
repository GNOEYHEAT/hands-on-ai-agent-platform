"""L2·L7 자동 검증: 도구 단위 검사 + 모의 모델로 대화 한 번(키 불필요).

    python labs/04-function-tools/check.py
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
from doc_report_agent.tools import analyze_document, read_document, save_report  # noqa: E402


def fail(msg: str) -> None:
    sys.exit(f"FAIL: {msg}")


async def converse(message: str) -> tuple[list[str], str]:
    runner = InMemoryRunner(agent=root_agent, app_name="check")
    session = await runner.session_service.create_session(app_name="check", user_id="student")
    calls, text = [], ""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    async for event in runner.run_async(user_id="student", session_id=session.id, new_message=content):
        calls += [fc.name for fc in event.get_function_calls()]
        if event.is_final_response() and event.content and event.content.parts:
            text += "".join(p.text or "" for p in event.content.parts)
    return calls, text


def main() -> None:
    if not isinstance(root_agent, LlmAgent) or root_agent.name != "doc_report_agent":
        fail("root_agent가 doc_report_agent라는 이름의 ADK Agent가 아닙니다")
    names = [t.__name__ for t in root_agent.tools]
    if names != ["read_document", "analyze_document", "save_report"]:
        fail(f"도구 목록이 다릅니다: {names}")
    print(f"root_agent: {root_agent.name}, tools: {', '.join(names)}")

    doc = read_document("samples/project_status_report.md")
    if doc["status"] != "success":
        fail(f"read_document가 샘플 문서를 읽지 못했습니다: {doc}")
    if read_document("../.env")["status"] != "error":
        fail("read_document가 data/ 밖 경로를 막지 않았습니다")
    analysis = analyze_document(doc["content"])
    if not analysis["issues"] or not analysis["key_points"]:
        fail(f"analyze_document 결과에 핵심 항목·문제점이 없습니다: {analysis}")
    print(f"analyze_document: 핵심 항목 {len(analysis['key_points'])}개, 문제점 {len(analysis['issues'])}개")
    saved = save_report("check report", "# check")
    if not (ROOT / saved["path"]).is_file():
        fail(f"save_report가 파일을 만들지 않았습니다: {saved}")
    (ROOT / saved["path"]).unlink()

    calls, text = asyncio.run(converse("샘플 보고서를 분석해 줘"))
    print(f"도구 호출 순서: {' -> '.join(calls)}")
    if calls != ["read_document", "analyze_document", "save_report"]:
        fail("모의 대화의 도구 호출 순서가 다릅니다")
    if "문제점" not in text or "outputs/" not in text:
        fail(f"최종 응답에 문제점·보고서 경로가 없습니다: {text}")
    print("최종 응답 마지막 줄: " + text.strip().splitlines()[-1])
    print("CHECK OK")


if __name__ == "__main__":
    main()
