# PART 3. AG-UI 기반 사용자 인터페이스 개발 (100분)

실습: L9 ADK 에이전트를 AG-UI로 노출(`labs/06-agui-backend`), L10 CopilotKit 채팅 화면(`labs/07-copilotkit-frontend`). 결과물: 웹 브라우저에서 실행되는 AI 에이전트.

## ① 강의 개요

- 학습 목표: ADK 에이전트를 AG-UI 엔드포인트로 열고, CopilotKit 화면으로 스트리밍 응답, 도구 실행 상태, 보고서 결과를 표시한다.
- 역할: 에이전트를 사용자가 쓰는 서비스 화면으로 만드는 단계.

## ② 개념 설명

- **Backend / Frontend**: Backend(ADK + `ag-ui-adk`, FastAPI, 8000번 포트)에서 에이전트가 돌고, Frontend(Next.js + CopilotKit, 3000번 포트)가 화면을 그린다.
- **AG-UI**: 에이전트 Backend와 사용자 화면 사이에 이벤트를 주고받는 오픈 프로토콜. 이벤트 종류는 Lifecycle(`RUN_STARTED`/`RUN_FINISHED`), Text Message, Tool Call, State.
- **AG-UI·MCP·A2A**: AG-UI(에이전트↔사용자), MCP(에이전트↔도구), A2A(에이전트↔에이전트)로 층이 다르다.
- **CopilotKit**: AG-UI를 쓰는 프론트엔드 프레임워크. AG-UI는 CopilotKit과 LangChain·CrewAI의 협력에서 출발한 프로토콜이고, CopilotKit은 그 프로토콜의 대표 구현이다. 둘은 같은 것이 아니다.
- **ADK와 AG-UI**: ADK는 AG-UI의 1st Party 지원 프레임워크다(출처는 [기술 검증 결과](../tech-verification.md)).

## ③ 아키텍처

[아키텍처 문서](../architecture.md)의 1~3번 그림을 쓴다. 브라우저(CopilotKit UI) → Next.js 런타임(`/api/copilotkit`) → AG-UI 엔드포인트(`/ag-ui`) → ADK 에이전트 → Gemini. 이벤트는 반대 방향으로 흐른다. 브라우저가 Gemini를 직접 부르지 않는다(SEC-03).

## ④ Hands-on

### L9 ADK 에이전트를 AG-UI로 노출 (`labs/06-agui-backend`, 25분)

터미널 1:

```
python labs/06-agui-backend/server.py
```

터미널 2:

```
python labs/06-agui-backend/send_run.py
```

모의 모델 기준 이벤트 순서: `RUN_STARTED` → (`TOOL_CALL_START` → `TOOL_CALL_ARGS` → `TOOL_CALL_END` → `TOOL_CALL_RESULT`)×3 → `TEXT_MESSAGE_START` → `TEXT_MESSAGE_CONTENT`(여러 번) → `TEXT_MESSAGE_END` → `STATE_SNAPSHOT` → `RUN_FINISHED`. 실제 모델은 도구 호출 전에 텍스트를 먼저 보낼 수 있다. 코드는 `labs/06-agui-backend/server.py`(`ADKAgent` + `add_adk_fastapi_endpoint`, CORS는 `http://localhost:3000`만).

```
python labs/06-agui-backend/check.py
```

8000 포트 충돌(`[Errno 10048]`)이 가장 흔하다.

### L10 CopilotKit 채팅 화면 (`labs/07-copilotkit-frontend`, 40분)

터미널 1에서 위의 서버를 띄운 채, 터미널 2에서:

```
npm --prefix labs/07-copilotkit-frontend install
```

```
npm --prefix labs/07-copilotkit-frontend run dev
```

http://localhost:3000 에서 `샘플 보고서를 분석해 줘`. 스트리밍 응답, 도구 상태 카드(`analyze_document 완료 핵심 항목 5개, 문제점 6개`), 오른쪽 '보고서 결과' 패널이 나오면 성공이다.

읽을 코드: `labs/07-copilotkit-frontend/app/api/copilotkit/[[...slug]]/route.ts`(런타임), `labs/07-copilotkit-frontend/app/page.tsx`(`CopilotChat`), `labs/07-copilotkit-frontend/app/components/ToolStatus.tsx`(`useRenderTool`). 확장 과제는 `read_document` 전용 카드 추가(`labs/07-copilotkit-frontend/README.md`).

```
python labs/07-copilotkit-frontend/check.py
```

| 오류 | 해결 |
| --- | --- |
| 답이 없다 | Backend 미기동 |
| `Agent 'doc_report_agent' not found` 류 | `app/agent.ts`의 `AGENT_ID`와 `route.ts`의 `agents` 키 불일치 |
| Backend 주소 변경 | 최상위 `.env`는 Next.js가 읽지 않는다. labs/07-copilotkit-frontend 폴더의 `.env.local` 사용 |
| Node 버전 | 20.9 이상(22 LTS 권장) |

## ⑤ 실습 확장

공유 상태, Human-in-the-loop(사람 확인), 생성형 UI는 CopilotKit이 제공하는 기능이며 이 실습에서는 구현하지 않았다.

## ⑥ 핵심 정리

- AG-UI 이벤트(`TEXT_MESSAGE_CONTENT`, `TOOL_CALL_*`)가 스트리밍과 도구 상태 카드를 만든다.
- AG-UI는 프로토콜, CopilotKit은 그 프로토콜의 프론트엔드 프레임워크.
- 키는 Backend에만. 다음 PART 4에서 이 서비스를 안전하게 만드는 방법을 본다.
