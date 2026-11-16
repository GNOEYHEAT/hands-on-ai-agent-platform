"""L8 자동 검증: MCP 서버 도구 목록·호출 + 모의 모델로 MCP 도구를 쓰는 대화 한 번(키 불필요).

    python labs/05-mcp-tools/check.py
"""
import asyncio
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ["DOC_AGENT_MODEL"] = "mock"  # .env보다 먼저 정해 모의 모델을 쓴다

from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from doc_report_agent.agent import doc_mcp_tools, root_agent  # noqa: E402


def fail(msg: str) -> None:
    sys.exit(f"FAIL: {msg}")


async def converse(message: str) -> tuple[list[str], str]:
    runner = InMemoryRunner(agent=root_agent, app_name="check")
    session = await runner.session_service.create_session(app_name="check", user_id="student")
    calls, text = [], ""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    try:
        async for event in runner.run_async(user_id="student", session_id=session.id, new_message=content):
            calls += [fc.name for fc in event.get_function_calls()]
            if event.is_final_response() and event.content and event.content.parts:
                text += "".join(p.text or "" for p in event.content.parts)
    finally:
        await doc_mcp_tools.close()  # MCP 서버 하위 프로세스를 닫는다
    return calls, text


async def mcp_tool_names() -> list[str]:
    try:
        return [tool.name for tool in await doc_mcp_tools.get_tools()]
    finally:
        await doc_mcp_tools.close()


def main() -> None:
    res = subprocess.run([sys.executable, str(HERE / "inspect_mcp.py")], capture_output=True,
                         text=True, encoding="utf-8", timeout=120, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if res.returncode != 0 or "list_documents" not in res.stdout or "read_document 결과: success" not in res.stdout:
        fail(f"inspect_mcp.py 실행 결과가 다릅니다\n{res.stdout}{res.stderr[-1500:]}")
    print("inspect_mcp.py: 도구 목록과 호출 결과 확인")

    names = asyncio.run(mcp_tool_names())
    if sorted(names) != ["list_documents", "read_document"]:
        fail(f"McpToolset이 가져온 도구가 다릅니다: {names}")
    print(f"McpToolset 도구: {', '.join(names)}")

    calls, text = asyncio.run(converse("샘플 문서를 분석해 줘"))
    print(f"도구 호출 순서: {' -> '.join(calls)}")
    if calls != ["list_documents", "read_document", "analyze_document", "save_report"]:
        fail("모의 대화의 도구 호출 순서가 다릅니다")
    if "문제점" not in text or "outputs/" not in text:
        fail(f"최종 응답에 문제점·보고서 경로가 없습니다: {text}")
    print("CHECK OK")


if __name__ == "__main__":
    main()
