# L8 MCP 서버로 문서 도구 연결

이 실습(advanced 트랙의 실습 8)에서는 문서 목록 보기와 문서 읽기 기능을 MCP 서버로 분리하고, ADK의 `McpToolset`으로 에이전트에 연결합니다. MCP(Model Context Protocol)는 에이전트가 외부 도구와 데이터에 표준 방식으로 연결하도록 정한 규격입니다. MCP 서버는 그 규격에 맞춰 도구를 제공하는 프로그램입니다.

## 구조

```
labs/05-mcp-tools/
├── doc_mcp_server.py   MCP 서버: list_documents, read_document (mcp SDK의 MCPServer)
├── inspect_mcp.py      MCP 클라이언트로 서버를 띄워 도구 목록·호출 결과를 출력
├── doc_report_agent/
│   ├── agent.py        McpToolset(StdioConnectionParams(...), tool_filter=[...]) + Function Tool 2개
│   ├── tools.py        analyze_document, save_report
│   └── mock_llm.py
└── check.py
```

MCP에서 에이전트(ADK)는 호스트, `McpToolset`은 클라이언트, `doc_mcp_server.py`는 서버입니다. 에이전트가 서버를 하위 프로세스로 직접 띄우고, 표준 입출력(stdio)으로 메시지를 주고받습니다. 표준 입출력은 프로그램이 글자를 읽고 쓰는 기본 통로입니다.

## 실행

가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널에서, 저장소 최상위 폴더에 있는 상태로 진행합니다.

1. MCP 서버를 직접 띄워 도구 목록과 호출 결과를 확인하세요.

   ```
   python labs/05-mcp-tools/inspect_mcp.py
   ```

2. ADK의 개발 UI를 띄우세요. 서버가 켜져 있는 동안 이 터미널은 그대로 두세요.

   ```
   adk web --port 8080 labs/05-mcp-tools
   ```

3. 브라우저 주소창에 http://localhost:8080 을 입력하고 `doc_report_agent`를 고르세요.
4. `샘플 문서를 분석해 줘`라고 입력하세요. 모의 모델 기준으로 `list_documents` → `read_document`(MCP 도구) → `analyze_document` → `save_report` 순서로 호출됩니다.

`inspect_mcp.py`의 출력은 다음과 같습니다.

```
MCP 서버 도구 목록:
  - list_documents: data/ 폴더 안에서 읽을 수 있는 문서(.md, .txt) 목록을 돌려준다.
  - read_document: data/ 폴더 안의 문서를 읽어 내용을 돌려준다.
list_documents 결과: samples/customer_feedback.txt, samples/injection_test.md, samples/meeting_notes.md, samples/project_status_report.md
read_document 결과: success, 첫 줄 = # 해커톤 팀 킥오프 회의록
data/ 밖 요청: error, data/ 폴더 밖은 읽을 수 없습니다: ../.env
```

## 핵심 규칙

- 서버를 띄우는 명령은 `python`이 아니라 `sys.executable`로 줍니다. `sys.executable`은 지금 실행 중인 Python의 경로입니다. 이렇게 해야 가상환경의 Python으로 서버가 뜹니다.
- MCP 서버 코드에서는 `print`를 쓰지 않습니다. stdout(표준 출력)이 MCP 메시지 통로라서, 다른 글자가 섞이면 통신이 깨집니다. 디버그 출력은 `sys.stderr`로 보내세요.
- `tool_filter`로 필요한 도구만 엽니다(SEC-06).
- mcp 2.x에서 서버 클래스는 `from mcp.server import MCPServer`입니다. 1.x에 있던 `FastMCP`(`mcp.server.fastmcp`)는 2.x에서 없어졌습니다.

## 확장: Goose에 같은 MCP 서버 붙이기

Goose Desktop 왼쪽 사이드바의 **익스텐션** 메뉴에서 확장을 추가하세요. 종류는 명령줄(STDIO) 확장으로 고르세요. 명령 칸에는 가상환경 Python의 경로와 `labs/05-mcp-tools/doc_mcp_server.py`의 절대 경로를 넣으세요. **익스텐션** 메뉴 이름은 스크린샷으로 확인했지만, 확장을 추가하는 화면 안의 항목 이름은 확인하지 못했습니다. 버전마다 다를 수 있습니다.

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/05-mcp-tools/check.py
```
