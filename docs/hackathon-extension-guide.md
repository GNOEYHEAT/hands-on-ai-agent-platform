# 해커톤 서비스 확장 가이드

문서 분석 에이전트의 뼈대를 그대로 두고 Instruction과 Tool만 바꾸면 내 서비스가 된다. 이 문서는 아이디어를 **역할(Instruction) + 도구(Tool) + 화면(AG-UI)** 세 칸으로 옮기는 방법과 도구를 늘리는 방법을 정리한다.

## 1. 아이디어를 세 칸으로

| 칸 | 질문 | 코드에서 바꿀 곳 |
| --- | --- | --- |
| 역할 | 누구를 돕고, 무엇을 하고, 어떻게 답하는가 | `labs/09-final-project/my_service_agent/agent.py`의 Instruction(TODO(2)) |
| 도구 | 답하려면 어떤 기능이 필요한가 | `labs/09-final-project/my_service_agent/tools.py`와 `agent.py`의 `tools=[...]`(TODO(1)) |
| 화면 | 사용자는 무엇을 보고 싶은가 | 기본은 `labs/07-copilotkit-frontend` 그대로. 새 도구는 `"*"` 카드로 표시 |

### 예시

| 아이디어 | 역할 | 도구 | 화면 |
| --- | --- | --- | --- |
| 고객 리뷰 분석 | 리뷰에서 불만과 개선점을 뽑아 주간 보고서를 쓴다 | 리뷰 읽기, 감성 분류, 보고서 저장 | 채팅 + 불만 순위 패널 |
| 회의록 할 일 정리 | 회의록에서 담당자·기한이 있는 할 일을 정리한다 | 할 일 추출(템플릿의 `extract_action_items`) | 채팅 + 할 일 목록 |
| 여행 일정 도우미 | 조건에 맞는 일정을 제안한다 | 일정 추출, 가격 비교 | 채팅 + 일정표 |

이 표는 발상용 예시이며 이 저장소에 구현되어 있지 않다.

## 2. 도구 하나 만드는 법

1. `tools.py`에 Python 함수를 만든다.
2. 인자에 타입 힌트, 함수에 docstring을 쓴다. 모델은 이 둘을 보고 도구를 고른다.
3. 반환은 `{"status": ..., ...}` 형태의 dict로 한다(성공과 실패를 구분).
4. `agent.py`의 `tools=[...]`에 넣는다.
5. `adk web --port 8080 labs/09-final-project`에서 시험하고 `python labs/09-final-project/check.py`를 통과시킨다.

파일을 읽는 도구라면 `data/` 밖을 읽지 못하게 한다(SEC-05).

## 3. 외부 API를 도구로 연결

외부 API(날씨, 지도, 결제 등)도 Function Tool 안에서 HTTP 호출을 하면 된다(`httpx`가 이미 설치되어 있다). 주의할 점:

- 외부 API 키도 `.env`에 두고 Backend에서만 읽는다(SEC-01, SEC-03).
- 외부에서 받은 내용은 지시가 아니라 데이터로 다룬다(SEC-07).
- 시연 중 네트워크가 끊길 수 있으니 실패 시 `{"status": "error", ...}`를 돌려주도록 한다.

## 4. MCP로 연결

여러 에이전트나 도구 앱이 같은 기능을 쓰게 하려면 MCP 서버로 분리한다. `labs/05-mcp-tools/doc_mcp_server.py`가 예제다. Python MCP SDK(`mcp` 2.3.0)의 `MCPServer`로 만들고, ADK에서는 `McpToolset`과 `tool_filter`로 필요한 도구만 연다(SEC-06). Goose에도 MCP 서버를 확장으로 붙일 수 있다. 화면 이름은 Goose 버전마다 다를 수 있어 확인하지 못했다.

공개 MCP 서버 중에는 Node.js의 `npx`가 필요한 것이 많다. 이 저장소의 실습은 Windows 준비 부담을 줄이려고 쓰지 않았다.

## 5. 화면을 더 풍부하게

CopilotKit은 채팅 외에 생성형 UI(도구 호출을 화면으로 렌더링), 공유 상태, 사람 확인(HITL)을 제공한다. 이 실습은 도구 상태 카드와 보고서 패널까지 구현했고, 나머지는 확장 주제로 남겼다. 먼저 `labs/07-copilotkit-frontend/app/components/ToolStatus.tsx`에 내 도구 전용 카드를 추가해 본다(`labs/07-copilotkit-frontend/README.md`의 '해 볼 것' 참고).

## 6. 시연 전 점검

- [ ] 데이터는 가상 데이터인가(SEC-09)
- [ ] 키가 저장소와 화면에 없는가(SEC-01, 03)
- [ ] 도구가 읽고 쓰는 범위가 제한되어 있는가(SEC-05)
- [ ] 키 없이도 시연할 대체 경로(모의 모델)가 있는가
- [ ] [보안·거버넌스 체크리스트](security-checklist.md)를 훑었는가
