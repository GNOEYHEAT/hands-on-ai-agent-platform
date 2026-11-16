"""L3·L10 자동 검증.

    python labs/07-copilotkit-frontend/check.py           # 정적 검사 + Backend AG-UI 왕복(Node.js 불필요)
    python labs/07-copilotkit-frontend/check.py --build   # 위 + npm install + npm run build
    python labs/07-copilotkit-frontend/check.py --e2e     # 위 + next dev를 띄워 CopilotKit 런타임 경유 왕복(node_modules 필요)
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BACKEND = ROOT / "labs" / "06-agui-backend"
AGENT_ID = "doc_report_agent"
DEFAULT_URL = "http://localhost:8000/ag-ui"
REQUIRED_PACKAGES = ["@copilotkit/react-core", "@copilotkit/runtime", "@ag-ui/client", "next", "react", "react-dom"]


def fail(msg: str) -> None:
    sys.exit(f"FAIL: {msg}")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for(port: int, proc: subprocess.Popen, name: str, seconds: int = 120) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if proc.poll() is not None:
            fail(f"{name}가 종료되었습니다")
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1).close()
            return
        except OSError:
            time.sleep(0.5)
    fail(f"{name}가 {seconds}초 안에 뜨지 않았습니다")


def stop(proc: subprocess.Popen) -> None:
    if os.name == "nt":  # npm·next가 만든 하위 프로세스까지 정리한다
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.kill()
    proc.wait()


def static_checks() -> None:
    pkg = json.loads((HERE / "package.json").read_text(encoding="utf-8"))
    deps = pkg.get("dependencies", {})
    missing = [name for name in REQUIRED_PACKAGES if name not in deps]
    if missing:
        fail(f"package.json에 패키지가 없습니다: {missing}")
    loose = [f"{n}@{v}" for n, v in deps.items() if not re.fullmatch(r"\d+\.\d+\.\d+", v)]
    if loose:
        fail(f"버전이 고정되지 않았습니다: {loose}")
    if not (HERE / "package-lock.json").is_file():
        fail("package-lock.json이 없습니다")

    route = (HERE / "app" / "api" / "copilotkit" / "[[...slug]]" / "route.ts").read_text(encoding="utf-8")
    if DEFAULT_URL not in route or "ADK_AG_UI_URL" not in route:
        fail(f"route.ts의 기본 AG-UI 주소가 {DEFAULT_URL}이 아니거나 ADK_AG_UI_URL을 읽지 않습니다")
    if not re.search(rf"agents:\s*\{{\s*{AGENT_ID}\s*:", route):
        fail(f"route.ts에 {AGENT_ID} 에이전트 등록이 없습니다")
    agent_ts = (HERE / "app" / "agent.ts").read_text(encoding="utf-8")
    if f'AGENT_ID = "{AGENT_ID}"' not in agent_ts:
        fail(f"app/agent.ts의 AGENT_ID가 {AGENT_ID}가 아닙니다")
    page = (HERE / "app" / "page.tsx").read_text(encoding="utf-8")
    if "agentId={AGENT_ID}" not in page:
        fail("page.tsx의 CopilotChat이 AGENT_ID를 쓰지 않습니다")

    # SEC-03: 브라우저 코드에 키가 없어야 한다
    for path in (HERE / "app").rglob("*.ts*"):
        text = path.read_text(encoding="utf-8")
        if "GOOGLE_API_KEY" in text or "NEXT_PUBLIC_" in text or re.search(r"AIza[0-9A-Za-z_\-]{20,}", text):
            fail(f"Frontend 코드에 키 관련 값이 있습니다: {path.relative_to(ROOT).as_posix()}")
    print(f"정적 검사: 패키지 고정, lock 파일, agentId={AGENT_ID}, 기본 URL={DEFAULT_URL}, 키 없음")


def start_backend(port: int) -> subprocess.Popen:
    env = dict(os.environ, DOC_AGENT_MODEL="mock", PORT=str(port), PYTHONIOENCODING="utf-8")
    proc = subprocess.Popen([sys.executable, str(BACKEND / "server.py")], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for(port, proc, "Backend(server.py)")
    return proc


def backend_roundtrip() -> None:
    port = free_port()
    backend = start_backend(port)
    try:
        res = subprocess.run([sys.executable, str(BACKEND / "send_run.py"), "--url", f"http://127.0.0.1:{port}/ag-ui"],
                             capture_output=True, text=True, encoding="utf-8", timeout=120, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    finally:
        stop(backend)
    types = [line.split()[0] for line in res.stdout.splitlines() if line.strip()]
    if res.returncode != 0 or "TOOL_CALL_START" not in types or types[-1:] != ["RUN_FINISHED"]:
        fail(f"Backend AG-UI 왕복 실패\n{res.stdout}{res.stderr}")
    print(f"Backend 왕복: 이벤트 {len(types)}개, RUN_STARTED ... RUN_FINISHED")


def npm(*args: str) -> None:
    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        fail("npm을 찾지 못했습니다(Node.js 설치 필요)")
    res = subprocess.run([npm_cmd, "--prefix", str(HERE), *args], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        fail(f"npm {' '.join(args)} 실패\n{res.stdout[-2000:]}{res.stderr[-2000:]}")
    print(f"npm {' '.join(args)}: 성공")


def runtime_roundtrip() -> None:
    next_bin = HERE / "node_modules" / ".bin" / ("next.cmd" if os.name == "nt" else "next")
    if not next_bin.exists():
        fail("node_modules가 없습니다. 먼저 npm --prefix labs/07-copilotkit-frontend install")
    backend_port, web_port = free_port(), free_port()
    backend = start_backend(backend_port)
    env = dict(os.environ, ADK_AG_UI_URL=f"http://127.0.0.1:{backend_port}/ag-ui",
               NEXT_TELEMETRY_DISABLED="1", COPILOTKIT_TELEMETRY_DISABLED="true")
    web = subprocess.Popen([str(next_bin), "dev", "--port", str(web_port)], cwd=HERE, env=env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=os.name == "nt")
    try:
        wait_for(web_port, web, "Frontend(next dev)")
        body = {"threadId": "check-thread", "runId": "check-run", "state": {}, "tools": [], "context": [],
                "forwardedProps": {}, "messages": [{"id": "m1", "role": "user", "content": "샘플 보고서를 분석해 줘"}]}
        req = urllib.request.Request(f"http://127.0.0.1:{web_port}/api/copilotkit/agent/{AGENT_ID}/run",
                                     data=json.dumps(body).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json", "Accept": "text/event-stream"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            lines = resp.read().decode("utf-8").splitlines()
    finally:
        stop(web)
        stop(backend)
    events = [json.loads(line[5:]) for line in lines if line.startswith("data:")]
    tools = [e.get("toolCallName") for e in events if e["type"] == "TOOL_CALL_START"]
    if not events or events[-1]["type"] != "RUN_FINISHED" or "analyze_document" not in tools:
        fail(f"CopilotKit 런타임 경유 왕복 실패: {[e['type'] for e in events]}")
    print(f"런타임 경유 왕복: /api/copilotkit -> /ag-ui, 도구 {', '.join(tools)}")


def main() -> None:
    static_checks()
    backend_roundtrip()
    if "--build" in sys.argv:
        npm("install")
        npm("run", "build")
    if "--e2e" in sys.argv:
        runtime_roundtrip()
    print("CHECK OK")


if __name__ == "__main__":
    main()
