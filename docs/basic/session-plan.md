# basic 60분 강의 구성표

초급, 60분, 개념 설명 30% / 실습 및 시연 70%. 사전 준비([사전 준비 가이드](../prep-guide.md))를 끝낸 상태로 시작한다. 실습 절차는 [README의 basic](../../README.md#basic)을 따른다.

| 시각 | 모듈 | 분 | 내용 | 실습(분) | 시연 |
| --- | --- | --- | --- | --- | --- |
| 0:00 | SESSION 1. AI 에이전트 플랫폼의 이해 | 5 | LLM vs 에이전트(1.5), 4계층과 오늘 만들 것(1.5), 사전 준비 점검·목차 | — | — |
| 0:05 | SESSION 2. Gemini API 연결 및 Goose 활용 | 10 | 키 → `.env` → 코드/Goose 흐름(2), L1, Goose 시연 | L1 (4) | Goose 설정·코드 생성 3.5분 |
| 0:15 | SESSION 3. AI 에이전트 개발 | 15 | 구성 요소 카드(3), `agent.py` 읽기(3.5), L2, MCP 개념 한 장 | L2 (8) | `agent.py` 읽기 3.5분 |
| 0:30 | SESSION 4. AG-UI를 활용한 채팅 화면 구현 | 20 | Backend/Frontend와 AG-UI 이벤트 흐름(4), L3, 최종 시연 | L3 (12) | 최종 시연 3.5분 |
| 0:50 | SESSION 5. 보안 및 해커톤 프로젝트 적용 | 10 | 체크리스트 핵심 6개(4), 내 아이디어를 세 칸으로(5.5) | — | — |
| 1:00 | 끝 | | | 합계 24분 | 약 10.5분 |

## 세션별 핵심 메시지

| 모듈 | 핵심 메시지 |
| --- | --- |
| SESSION 1 | AI 모델을 직접 개발하지 않아도 API를 활용하면 나만의 AI 에이전트 서비스를 만들 수 있다 |
| SESSION 2 | 키 하나와 모델 ID 하나로 어떤 도구에서든 같은 Gemini를 쓴다 |
| SESSION 3 | ADK 에이전트는 Model + Instruction + Tool 세 줄로 시작한다 |
| SESSION 4 | 에이전트는 Backend에서 동작하지만 AG-UI를 통해 사용자에게 친숙한 서비스 화면으로 제공할 수 있다 |
| SESSION 5 | 키는 백엔드에, 권한은 최소로, 문서는 데이터로 |

## 쓰는 실습 폴더

| basic 실습 | 폴더 | 명령 |
| --- | --- | --- |
| L1 | `labs/01-gemini-api` | `python labs/01-gemini-api/hello_gemini.py` |
| L2 | `labs/04-function-tools` | `adk web --port 8080 labs/04-function-tools` |
| L3 | `labs/06-agui-backend` + `labs/07-copilotkit-frontend` | `python labs/06-agui-backend/server.py`, `npm --prefix labs/07-copilotkit-frontend run dev` |

## 운영 팁

- 사전 준비가 안 된 참가자는 모의 모델(`--mock`, `DOC_AGENT_MODEL=mock`)로 따라오게 한다. 흐름과 화면은 같다.
- 시간이 밀리면 SESSION 4의 L3를 참가자 실습에서 강사 시연으로 바꾼다([데모 시나리오](demo-scenario.md)의 대체 경로).
- Goose는 GUI라 시연으로 진행한다. 직접 해 보고 싶은 사람은 advanced L5로 안내한다.
- 포트: `adk web` 8080, Backend 8000, Frontend 3000. 포트 충돌이 가장 흔한 막힘이다.
- 시연 전에 `labs/07-copilotkit-frontend`의 `npm install`이 끝나 있는지 확인한다(약 5분).
