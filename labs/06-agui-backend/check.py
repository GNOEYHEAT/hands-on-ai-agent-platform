"""L9 자동 검증: 모의 모델로 server.py를 빈 포트에 띄우고 send_run.py로 AG-UI 이벤트 순서를 확인한다(키 불필요).

    python labs/06-agui-backend/check.py
"""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = ["RUN_STARTED", "TOOL_CALL_START", "TOOL_CALL_ARGS", "TOOL_CALL_END", "TOOL_CALL_RESULT",
            "TEXT_MESSAGE_START", "TEXT_MESSAGE_CONTENT", "TEXT_MESSAGE_END", "RUN_FINISHED"]


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for(port: int, server: subprocess.Popen, seconds: int = 60) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if server.poll() is not None:
            sys.exit(f"FAIL: server.py가 종료되었습니다\n{server.stdout.read()}")
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1).close()
            return
        except OSError:
            time.sleep(0.5)
    sys.exit("FAIL: server.py가 시간 안에 뜨지 않았습니다")


def main() -> None:
    port = free_port()
    env = dict(os.environ, DOC_AGENT_MODEL="mock", PORT=str(port), PYTHONIOENCODING="utf-8")
    server = subprocess.Popen([sys.executable, str(HERE / "server.py")], env=env, text=True,
                              encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        wait_for(port, server)
        res = subprocess.run([sys.executable, str(HERE / "send_run.py"), "--url", f"http://127.0.0.1:{port}/ag-ui"],
                             capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
    finally:
        server.kill()
        server.wait()
    if res.returncode != 0:
        sys.exit(f"FAIL: send_run.py 종료 코드 {res.returncode}\n{res.stdout}{res.stderr}")
    types = [line.split()[0] for line in res.stdout.splitlines() if line.strip()]
    missing = [t for t in REQUIRED if t not in types]
    if missing:
        sys.exit(f"FAIL: 이벤트가 빠졌습니다: {missing}\n{res.stdout}")
    if types[0] != "RUN_STARTED" or types[-1] != "RUN_FINISHED":
        sys.exit(f"FAIL: 첫 이벤트는 RUN_STARTED, 마지막은 RUN_FINISHED여야 합니다: {types}")
    tools = [line.split()[1] for line in res.stdout.splitlines() if line.startswith("TOOL_CALL_START")]
    # 같은 이벤트가 이어지면 한 번만 적어 순서를 짧게 보여 준다
    order = [t for i, t in enumerate(types) if i == 0 or t != types[i - 1]]
    print("이벤트 순서: " + " -> ".join(order))
    print(f"TOOL_CALL_START 도구: {', '.join(tools)} / TEXT_MESSAGE_CONTENT {types.count('TEXT_MESSAGE_CONTENT')}회")
    print("CHECK OK")


if __name__ == "__main__":
    main()
