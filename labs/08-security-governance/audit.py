"""보안·거버넌스 체크리스트(SEC-01~SEC-12) 중 자동으로 확인할 수 있는 항목을 점검한다.

    python labs/08-security-governance/audit.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from doc_report_agent.guardrails import INJECTION_PATTERNS, mask  # noqa: E402
from doc_report_agent.tools import read_document  # noqa: E402

KEY_RE = re.compile(r"AIza[0-9A-Za-z_\-]{30,}")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".next", "__pycache__", "outputs", "logs", ".adk"}
TEXT_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".json", ".md", ".txt", ".toml", ".yaml", ".yml", ".example", ""}
MANUAL = {
    "SEC-04": "사용자를 식별·인증하고 사용자별 권한을 나눈다",
    "SEC-06": "MCP 도구는 tool_filter로 필요한 것만 열고, 위험한 도구는 실행 전 사용자 승인을 받는다",
    "SEC-09": "무료 등급 입력은 제품 개선에 쓰일 수 있으므로 민감·개인 정보를 넣지 않는다",
    "SEC-10": "사용량·비용 한도와 결제 알림을 설정한다",
    "SEC-12": "키가 유출되면 새 키 발급 -> 교체 -> 옛 키 비활성화 -> 사용 기록 확인",
}


def repo_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not SKIP_DIRS.intersection(path.relative_to(ROOT).parts) and path.name != ".env":
            if path.suffix in TEXT_SUFFIXES:
                yield path


def sec01() -> tuple[bool, str]:
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    if ".env" not in ignored:
        return False, ".gitignore에 .env가 없습니다"
    leaked = [p.relative_to(ROOT).as_posix() for p in repo_files()
              if KEY_RE.search(p.read_text(encoding="utf-8", errors="ignore"))]
    return (not leaked, "코드에 키 형태 문자열 없음, .env는 .gitignore" if not leaked else f"키 의심: {leaked}")


def sec02() -> tuple[bool, str]:
    example = ROOT / ".env.example"
    if not example.is_file():
        return False, ".env.example이 없습니다"
    values = dict(line.split("=", 1) for line in example.read_text(encoding="utf-8").splitlines()
                  if "=" in line and not line.startswith("#"))
    return (values.get("GOOGLE_API_KEY", "x").strip() == "", ".env.example의 GOOGLE_API_KEY 값이 비어 있음")


def sec03() -> tuple[bool, str]:
    app = ROOT / "labs" / "07-copilotkit-frontend" / "app"
    bad = [p.relative_to(ROOT).as_posix() for p in app.rglob("*.ts*")
           if re.search(r"GOOGLE_API_KEY|NEXT_PUBLIC_|AIza", p.read_text(encoding="utf-8"))]
    return (not bad, "Frontend 코드에 키 없음(Backend 경유)" if not bad else f"Frontend에 키 관련 값: {bad}")


def sec05() -> tuple[bool, str]:
    attempts = ["../.env", "../../secret.txt", str(ROOT / ".env")]
    allowed = [a for a in attempts if read_document(a)["status"] != "error"]
    ok = not allowed and read_document("samples/meeting_notes.md")["status"] == "success"
    return ok, "data/ 밖 경로 3건 거부, data/ 안 문서는 읽기 허용" if ok else f"막지 못한 경로: {allowed}"


def sec07() -> tuple[bool, str]:
    text = (ROOT / "data" / "samples" / "injection_test.md").read_text(encoding="utf-8")
    hits = [p for p in INJECTION_PATTERNS if re.search(p, text, re.IGNORECASE)]
    return bool(hits), f"injection_test.md에서 인젝션 패턴 {len(hits)}개 탐지"


def sec08() -> tuple[bool, str]:
    sample = "GOOGLE_API_KEY=abc123 AIza" + "X" * 35
    masked = mask(sample)
    ok = "abc123" not in masked and "AIza" not in masked
    return ok, "실행 로그의 키 값 가림 처리 확인" if ok else f"가림 실패: {masked}"


def sec11() -> tuple[bool, str]:
    server = (ROOT / "labs" / "06-agui-backend" / "server.py").read_text(encoding="utf-8")
    match = re.search(r"allow_origins\s*=\s*\[([^\]]*)\]", server)
    ok = bool(match) and "*" not in match.group(1)
    return ok, f"CORS 허용 출처 {match.group(1).strip() if match else '(설정 없음)'}"


def main() -> int:
    checks = {"SEC-01": sec01, "SEC-02": sec02, "SEC-03": sec03, "SEC-05": sec05,
              "SEC-07": sec07, "SEC-08": sec08, "SEC-11": sec11}
    failed = 0
    for sec_id, check in checks.items():
        ok, message = check()
        failed += not ok
        print(f"{sec_id} {'PASS' if ok else 'FAIL'}  {message}")
    for sec_id, text in MANUAL.items():
        print(f"{sec_id} 수동  {text}")
    print(f"자동 점검 {len(checks)}개 중 PASS {len(checks) - failed}개, FAIL {failed}개")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
