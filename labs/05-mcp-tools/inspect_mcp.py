"""MCP 클라이언트로 doc_mcp_server.py를 띄워 도구 목록을 보고 직접 호출해 본다(키 불필요).

    python labs/05-mcp-tools/inspect_mcp.py
"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client

SERVER = Path(__file__).resolve().parent / "doc_mcp_server.py"


def as_dict(result) -> dict:
    """도구 결과(TextContent에 담긴 JSON 문자열)를 dict로 바꾼다."""
    return json.loads(result.content[0].text)


async def main() -> None:
    # sys.executable: 지금 실행 중인 가상환경의 파이썬으로 서버를 띄운다
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("MCP 서버 도구 목록:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description.splitlines()[0]}")

            listed = as_dict(await session.call_tool("list_documents", {}))
            print("list_documents 결과:", ", ".join(listed["documents"]))

            doc = as_dict(await session.call_tool("read_document", {"path": "samples/meeting_notes.md"}))
            print(f"read_document 결과: {doc['status']}, 첫 줄 = {doc['content'].splitlines()[0]}")

            blocked = as_dict(await session.call_tool("read_document", {"path": "../.env"}))
            print(f"data/ 밖 요청: {blocked['status']}, {blocked['message']}")


if __name__ == "__main__":
    asyncio.run(main())
