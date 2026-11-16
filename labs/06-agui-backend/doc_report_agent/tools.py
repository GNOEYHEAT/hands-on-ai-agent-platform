"""문서 분석 Function Tool 3개. 타입 힌트와 docstring이 그대로 모델에게 주는 도구 설명이 된다."""
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # 저장소 최상위
DATA_DIR = ROOT / "data"                      # 읽기 허용 폴더
OUTPUT_DIR = ROOT / "outputs"                 # 쓰기 허용 폴더
ALLOWED_SUFFIXES = {".md", ".txt"}
ISSUE_KEYWORDS = ("위험", "지연", "TODO", "오류", "불편", "느립")


def read_document(path: str) -> dict:
    """data/ 폴더 안의 문서(.md, .txt)를 읽어 내용을 돌려준다.

    Args:
        path: data/ 기준 상대 경로. 예: "samples/project_status_report.md"
    """
    relative = path.replace("\\", "/").removeprefix("data/")
    target = (DATA_DIR / relative).resolve()
    if not target.is_relative_to(DATA_DIR.resolve()):
        return {"status": "error", "message": f"data/ 폴더 밖은 읽을 수 없습니다: {path}"}
    if target.suffix not in ALLOWED_SUFFIXES or not target.is_file():
        return {"status": "error", "message": f"읽을 수 있는 .md/.txt 문서가 아닙니다: {path}"}
    return {"status": "success", "path": relative, "content": target.read_text(encoding="utf-8")}


def analyze_document(text: str) -> dict:
    """문서 내용에서 제목, 소제목, 핵심 항목, 문제점(위험·지연·TODO 등)을 규칙으로 뽑는다.

    Args:
        text: 분석할 문서 내용 전체
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = next((l.lstrip("# ") for l in lines if l.startswith("# ")), lines[0] if lines else "")
    bullets = [re.sub(r"^(-|\d+\.)\s+", "", l) for l in lines if re.match(r"^(-|\d+\.)\s+", l)]
    issues = [b for b in bullets if any(k in b for k in ISSUE_KEYWORDS)]
    return {
        "status": "success",
        "title": title,
        "headings": [l.lstrip("# ") for l in lines if l.startswith("## ")],
        "line_count": len(lines),
        "key_points": [b for b in bullets if b not in issues][:5],
        "issues": issues,
    }


def save_report(title: str, markdown: str) -> dict:
    """작성한 보고서(Markdown)를 outputs/ 폴더에 저장하고 저장 경로를 돌려준다.

    Args:
        title: 보고서 제목. 파일 이름으로 쓴다
        markdown: 보고서 본문(Markdown)
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    name = re.sub(r"[^\w\-]+", "_", title).strip("_")[:40] or "report"
    target = OUTPUT_DIR / f"{datetime.now():%Y%m%d-%H%M%S}_{name}.md"
    target.write_text(markdown, encoding="utf-8")
    return {"status": "success", "path": f"outputs/{target.name}"}
