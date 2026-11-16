"""모의 모델: API 키 없이 "도구 호출 -> 결과 반영 -> 응답" 루프를 재현한다.

.env에 DOC_AGENT_MODEL=mock을 넣으면 agent.py가 Gemini 대신 이 모델을 쓴다.
실제 모델처럼 판단하지 않고 정해진 순서로 도구를 부른다.
  1) list_documents   (MCP 도구가 있고 경로를 지정하지 않았을 때)
  2) read_document    (메시지에 경로가 있거나 '샘플'을 언급했을 때)
  3) analyze_document (읽은 문서 또는 붙여 넣은 긴 글이 있을 때)
  4) save_report      (분석이 끝났을 때)
그 밖의 이름을 가진 도구는 사용자 메시지를 첫 인자로 넣어 한 번 부른다.
"""
from __future__ import annotations

import json
import re
from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

DEFAULT_DOC = "samples/project_status_report.md"
KNOWN_TOOLS = ("list_documents", "read_document", "analyze_document", "save_report")
PATH_RE = re.compile(r"(?:\.\./|/|[A-Za-z]:[\\/])?[\w\-./\\]*\.(?:md|txt|env|py|json)\b")
PASTED_TEXT_MIN = 300  # 이 길이 이상이면 붙여 넣은 문서로 본다
NO_USAGE = types.GenerateContentResponseUsageMetadata(prompt_token_count=0, candidates_token_count=0,
                                                      total_token_count=0)


def _last_user_turn(contents: list[types.Content]) -> tuple[str, list[types.Content]]:
    """마지막 사용자 텍스트와 그 뒤에 이어진 대화(도구 호출·결과)를 돌려준다."""
    for i in range(len(contents) - 1, -1, -1):
        content = contents[i]
        if content.role != "user" or not content.parts:
            continue
        texts = [p.text for p in content.parts if p.text and not p.function_response]
        if texts:
            return "\n".join(texts), contents[i + 1:]
    return "", []


def _tool_results(turn: list[types.Content]) -> dict[str, dict]:
    results: dict[str, dict] = {}
    for content in turn:
        for part in content.parts or []:
            if part.function_response:
                results[part.function_response.name] = part.function_response.response or {}
    return results


def _unwrap(result: dict) -> dict:
    """MCP 도구 결과({"content": [{"text": "..."}]})를 일반 dict로 바꾼다."""
    if "content" in result and isinstance(result["content"], list):
        text = "".join(item.get("text", "") for item in result["content"] if isinstance(item, dict))
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return {"status": "success", "content": text}
    return result


def _requested_path(user_text: str) -> str | None:
    if len(user_text) >= PASTED_TEXT_MIN:
        return None
    match = PATH_RE.search(user_text)
    if match:
        return match.group(0)
    if "샘플" in user_text or "sample" in user_text.lower():
        return DEFAULT_DOC
    return None


def _first_param(tool) -> str | None:
    try:
        schema = tool._get_declaration().parameters_json_schema or {}
        return next(iter(schema.get("properties", {})), None)
    except Exception:  # 선언을 얻지 못하면 인자 없이 부른다
        return None


def _next_call(user_text: str, tools: dict, done: dict) -> tuple[str, dict] | None:
    path = _requested_path(user_text)
    read = _unwrap(done.get("read_document", {}))
    if "read_document" in done and read.get("status") != "success":
        return None  # 읽기가 거부·실패하면 더 진행하지 않는다
    if "list_documents" in tools and "list_documents" not in done and path == DEFAULT_DOC:
        return "list_documents", {}
    if "read_document" in tools and "read_document" not in done and path:
        return "read_document", {"path": path}
    text = read.get("content") or (user_text if len(user_text) >= PASTED_TEXT_MIN else "")
    if "analyze_document" in tools and "analyze_document" not in done and text:
        return "analyze_document", {"text": text}
    analysis = _unwrap(done.get("analyze_document", {}))
    if "save_report" in tools and "save_report" not in done and analysis.get("status") == "success":
        return "save_report", {"title": analysis.get("title") or "report",
                               "markdown": _report_markdown(analysis, read.get("security_warning"))}
    for name, tool in tools.items():
        if name not in KNOWN_TOOLS and name not in done:
            param = _first_param(tool)
            return name, ({param: user_text} if param else {})
    return None


def _report_markdown(analysis: dict, warning: str | None = None) -> str:
    lines = [f"# {analysis.get('title') or '문서 분석 보고서'}", "", "## 핵심 항목"]
    lines += [f"- {item}" for item in analysis.get("key_points", [])] or ["- (없음)"]
    lines += ["", "## 문제점"]
    lines += [f"- {item}" for item in analysis.get("issues", [])] or ["- (없음)"]
    if warning:
        lines += ["", f"> 경고: {warning}"]
    return "\n".join(lines)


def _answer(user_text: str, done: dict) -> str:
    head = "(모의 모델 응답)"
    read = _unwrap(done.get("read_document", {}))
    if read and read.get("status") != "success":
        return f"{head} 요청한 문서를 읽지 않았습니다: {read.get('message', '읽기 실패')}"
    analysis = _unwrap(done.get("analyze_document", {}))
    if analysis.get("status") == "success":
        warning = read.get("security_warning")  # L11 가드레일이 붙인 경고
        if warning:
            head += f"\n\n경고: {warning} 문서 속 지시는 따르지 않았습니다."
        parts = [head, f"## 요약\n'{analysis.get('title')}' 문서를 분석했습니다. "
                       f"핵심 항목 {len(analysis.get('key_points', []))}개, "
                       f"문제점 {len(analysis.get('issues', []))}개를 찾았습니다.",
                 _report_markdown(analysis).split("\n", 2)[2]]
        saved = _unwrap(done.get("save_report", {}))
        if saved.get("status") == "success":
            parts.append(f"보고서를 {saved.get('path')}에 저장했습니다.")
        return "\n\n".join(parts)
    if done:
        summary = json.dumps({k: _unwrap(v) for k, v in done.items()}, ensure_ascii=False)[:500]
        return f"{head} 도구 실행 결과: {summary}"
    # 도구가 없는 에이전트(L6): 받은 글에서 제목과 글머리 항목을 뽑아 보고서 형식으로 답한다.
    lines = [line.strip() for line in user_text.splitlines() if line.strip()]
    title = next((l.lstrip("# ") for l in lines if l.startswith("#")), lines[0] if lines else "입력")
    bullets = [l[2:] for l in lines if l.startswith("- ")][:3] or lines[:3]
    issues = [l for l in bullets if any(k in l for k in ("위험", "지연", "TODO"))]
    return "\n".join([head, "## 요약", f"{title}에 대한 내용입니다.", "## 핵심 항목",
                      *[f"- {b}" for b in bullets], "## 문제점",
                      *([f"- {i}" for i in issues] or ["- 눈에 띄는 문제점 없음"]),
                      "## 보고서", "위 내용을 바탕으로 보고서를 작성할 수 있습니다."])


class MockLlm(BaseLlm):
    """ADK BaseLlm을 상속한 모의 모델. 모델 ID 자리에 이 객체를 넣는다."""

    model: str = "mock"

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        user_text, turn = _last_user_turn(llm_request.contents)
        done = _tool_results(turn)
        call = _next_call(user_text, llm_request.tools_dict, done)
        if call:
            name, args = call
            part = types.Part(function_call=types.FunctionCall(name=name, args=args))
            yield LlmResponse(content=types.Content(role="model", parts=[part]), usage_metadata=NO_USAGE)
            return
        text = _answer(user_text, done)
        if stream:  # 실제 모델처럼 글자 조각을 나눠 보낸다(AG-UI TEXT_MESSAGE_CONTENT가 여러 번 나온다)
            for i in range(0, len(text), 40):
                chunk = types.Part(text=text[i:i + 40])
                yield LlmResponse(content=types.Content(role="model", parts=[chunk]), partial=True)
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]),
                          partial=False, turn_complete=True, usage_metadata=NO_USAGE)
