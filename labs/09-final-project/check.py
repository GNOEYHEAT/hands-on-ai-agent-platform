"""L12 자동 검증: 템플릿(또는 내가 바꾼) my_service_agent가 도구를 부르고 답하는지, AG-UI 서버로 열리는지 확인한다.

    python labs/09-final-project/check.py
"""
import asyncio
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
os.environ["DOC_AGENT_MODEL"] = "mock"  # .env보다 먼저 정해 모의 모델을 쓴다

from google.adk.agents import LlmAgent  # noqa: E402
from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from my_service_agent.agent import root_agent  # noqa: E402

SAMPLE = (ROOT / "data" / "samples" / "meeting_notes.md").read_text(encoding="utf-8")


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


def agui_roundtrip() -> list[str]:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, PORT=str(port), PYTHONIOENCODING="utf-8")
    server = subprocess.Popen([sys.executable, str(HERE / "server.py")], env=env,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            if server.poll() is not None:
                fail("server.py가 종료되었습니다")
            try:
                socket.create_connection(("127.0.0.1", port), timeout=1).close()
                break
            except OSError:
                time.sleep(0.5)
        body = {"threadId": "check", "runId": "check-run", "state": {}, "tools": [], "context": [],
                "forwardedProps": {}, "messages": [{"id": "m1", "role": "user", "content": SAMPLE}]}
        with httpx.stream("POST", f"http://127.0.0.1:{port}/ag-ui", json=body, timeout=120) as resp:
            return [json.loads(line[5:])["type"] for line in resp.iter_lines() if line.startswith("data:")]
    finally:
        server.kill()
        server.wait()


def main() -> None:
    if not isinstance(root_agent, LlmAgent) or not root_agent.tools:
        fail("root_agent가 도구를 가진 ADK Agent가 아닙니다")
    names = [getattr(t, "__name__", getattr(t, "name", "?")) for t in root_agent.tools]
    undocumented = [n for n, t in zip(names, root_agent.tools) if callable(t) and not (t.__doc__ or "").strip()]
    if undocumented:
        fail(f"docstring이 없는 도구가 있습니다(모델이 도구를 고르지 못함): {undocumented}")
    print(f"root_agent: {root_agent.name}, tools: {', '.join(names)}")

    calls, text = asyncio.run(converse(SAMPLE))
    if not calls or not text.strip():
        fail(f"모의 대화에서 도구 호출이나 응답이 없습니다: calls={calls}, text={text!r}")
    print(f"모의 대화: 도구 {', '.join(calls)} 호출 후 응답")

    events = agui_roundtrip()
    if not events or events[0] != "RUN_STARTED" or events[-1] != "RUN_FINISHED" or "TOOL_CALL_START" not in events:
        fail(f"AG-UI 이벤트가 다릅니다: {events}")
    print(f"server.py AG-UI 왕복: RUN_STARTED ... TOOL_CALL_START ... RUN_FINISHED ({len(events)}개 이벤트)")
    print("CHECK OK")


if __name__ == "__main__":
    main()
