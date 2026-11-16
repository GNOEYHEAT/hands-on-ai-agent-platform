"""L1·L4 자동 검증. 기본은 키 없이 모의 경로로 확인하고, --live를 주면 실제 API를 부른다.

    python labs/01-gemini-api/check.py
    python labs/01-gemini-api/check.py --live   # GOOGLE_API_KEY가 있을 때만
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, *args: str) -> str:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    res = subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True,
                         text=True, encoding="utf-8", env=env)
    if res.returncode != 0:
        print(res.stdout, res.stderr)
        sys.exit(f"FAIL: {script} {' '.join(args)} 종료 코드 {res.returncode}")
    return res.stdout


def main() -> None:
    live = "--live" in sys.argv
    mode = [] if live else ["--mock"]
    if live and not os.getenv("GOOGLE_API_KEY"):
        sys.exit("FAIL: --live에는 GOOGLE_API_KEY가 필요합니다")

    out = run("list_models.py", *mode)
    if ": available" not in out:
        sys.exit(f"FAIL: list_models.py 출력에 'available'이 없습니다\n{out}")
    print("list_models.py: " + out.strip().splitlines()[-1])

    out = run("hello_gemini.py", *mode)
    if "모델 ID:" not in out or "요약:" not in out:
        sys.exit(f"FAIL: hello_gemini.py 출력에 모델 ID와 요약이 없습니다\n{out}")
    summary = out.split("요약:", 1)[1].strip()
    if not summary:
        sys.exit("FAIL: 요약이 비어 있습니다")
    print("hello_gemini.py: " + out.strip().splitlines()[0])
    print(f"요약 {len(summary.splitlines())}줄 확인 ({'실제 호출' if live else '모의 경로'})")
    print("CHECK OK")


if __name__ == "__main__":
    main()
