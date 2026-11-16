"""문서 목록·읽기 MCP 서버(stdio). data/ 폴더 안의 .md/.txt 문서만 제공한다.

ADK 에이전트(McpToolset)나 inspect_mcp.py가 이 파일을 하위 프로세스로 띄워 표준 입출력으로 대화한다.
stdout은 MCP 메시지 통로이므로 print를 쓰지 않는다(디버그 출력은 sys.stderr로).
"""
from pathlib import Path

from mcp.server import MCPServer

ROOT = Path(__file__).resolve().parents[2]   # 저장소 최상위
DATA_DIR = (ROOT / "data").resolve()          # 이 서버가 열어 주는 유일한 폴더
ALLOWED_SUFFIXES = {".md", ".txt"}

mcp = MCPServer("doc-mcp-server")


@mcp.tool()
def list_documents() -> dict:
    """data/ 폴더 안에서 읽을 수 있는 문서(.md, .txt) 목록을 돌려준다."""
    files = sorted(p.relative_to(DATA_DIR).as_posix() for p in DATA_DIR.rglob("*")
                   if p.suffix in ALLOWED_SUFFIXES and p.is_file())
    return {"status": "success", "documents": files}


@mcp.tool()
def read_document(path: str) -> dict:
    """data/ 폴더 안의 문서를 읽어 내용을 돌려준다.

    Args:
        path: data/ 기준 상대 경로. 예: "samples/project_status_report.md"
    """
    relative = path.replace("\\", "/").removeprefix("data/")
    target = (DATA_DIR / relative).resolve()
    if not target.is_relative_to(DATA_DIR):
        return {"status": "error", "message": f"data/ 폴더 밖은 읽을 수 없습니다: {path}"}
    if target.suffix not in ALLOWED_SUFFIXES or not target.is_file():
        return {"status": "error", "message": f"읽을 수 있는 .md/.txt 문서가 아닙니다: {path}"}
    return {"status": "success", "path": relative, "content": target.read_text(encoding="utf-8")}


if __name__ == "__main__":
    mcp.run()  # 기본 전송 방식: stdio
