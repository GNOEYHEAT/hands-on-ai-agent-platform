"""가드레일 3종: ADK 콜백으로 도구 실행 전후를 검사하고 기록한다.

- block_outside_data   (before_tool_callback) data/ 밖 경로 읽기를 막는다(SEC-05)
- flag_prompt_injection(after_tool_callback)  읽은 문서의 숨은 지시를 찾아 경고를 붙인다(SEC-07)
- write_audit_log      (after_tool_callback)  도구 호출을 logs/agent_audit.jsonl에 기록한다(SEC-08)
콜백이 None을 돌려주면 그대로 진행하고, dict를 돌려주면 그 값이 도구 결과를 대신한다.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = (ROOT / "data").resolve()
LOG_FILE = ROOT / "logs" / "agent_audit.jsonl"

INJECTION_PATTERNS = [
    r"(이전|앞의|위의)\s*(모든\s*)?(지시|명령|규칙)[을를]?\s*(모두\s*)?무시",
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"system\s*prompt",
    r"\.env\b",
]
SECRET_PATTERNS = [r"AIza[0-9A-Za-z_\-]{20,}", r"(GOOGLE_API_KEY|GEMINI_API_KEY)\s*=\s*\S+"]


def mask(text: str) -> str:
    """로그에 비밀 값이 남지 않게 가린다."""
    for pattern in SECRET_PATTERNS:
        text = re.sub(pattern, "***", text)
    return text


def block_outside_data(tool, args: dict, tool_context) -> dict | None:
    """read_document의 경로가 data/ 밖이면 도구를 실행하지 않고 거부 결과를 돌려준다."""
    if tool.name != "read_document":
        return None
    relative = str(args.get("path", "")).replace("\\", "/").removeprefix("data/")
    if (DATA_DIR / relative).resolve().is_relative_to(DATA_DIR):
        return None
    result = {"status": "error", "blocked_by": "guardrail",
              "message": f"보안 정책: data/ 폴더 밖 경로는 읽을 수 없습니다 ({args.get('path')})"}
    _append_log(tool.name, args, tool_context, result, blocked=True)
    return result


def flag_prompt_injection(tool, args: dict, tool_context, tool_response: dict) -> dict | None:
    """읽은 문서에 숨은 지시가 있으면 결과에 경고를 붙인다. 문서 내용은 지시가 아니라 데이터다."""
    if tool.name != "read_document" or tool_response.get("status") != "success":
        return None
    found = [p for p in INJECTION_PATTERNS if re.search(p, tool_response.get("content", ""), re.IGNORECASE)]
    if not found:
        return None
    return {**tool_response, "security_warning": "문서에 에이전트 지시를 바꾸려는 문장(프롬프트 인젝션 의심)이 있습니다."}


def write_audit_log(tool, args: dict, tool_context, tool_response: dict) -> None:
    """모든 도구 호출을 기록한다. None을 돌려주므로 결과는 바뀌지 않는다."""
    _append_log(tool.name, args, tool_context, tool_response, blocked=False)
    return None


def after_tool_guard(tool, args: dict, tool_context, tool_response: dict) -> dict | None:
    """after_tool_callback: 인젝션 검사 후 (경고가 붙은) 결과를 기록한다."""
    if tool_response.get("blocked_by") == "guardrail":   # 차단은 block_outside_data가 이미 기록했다
        return None
    flagged = flag_prompt_injection(tool, args, tool_context, tool_response)
    write_audit_log(tool, args, tool_context, flagged or tool_response)
    return flagged


def _append_log(tool_name: str, args: dict, tool_context, result: dict, blocked: bool) -> None:
    LOG_FILE.parent.mkdir(exist_ok=True)
    entry = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user": getattr(tool_context, "user_id", "unknown"),
        "tool": tool_name,
        "args": {k: mask(str(v))[:80] for k, v in args.items()},   # 긴 인자는 앞부분만
        "status": result.get("status"),
        "blocked": blocked,
        "warning": result.get("security_warning"),
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
