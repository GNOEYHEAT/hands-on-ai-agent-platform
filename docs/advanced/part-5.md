# PART 5. 나만의 AI 에이전트 프로토타입 (30분)

실습: L12 나만의 에이전트 프로토타입(`labs/09-final-project`). 최종 결과물: 각자의 서비스 아이디어를 반영한 AI 에이전트 프로토타입. 진행과 평가는 [최종 프로젝트 가이드](final-project-guide.md)에 자세히 있다.

## ① 강의 개요

- 학습 목표: 서비스 아이디어를 에이전트 역할·도구·화면으로 설계하고 프로토타입을 만든다.
- 핵심 메시지: 문서 분석 에이전트의 뼈대를 그대로 두고 Instruction과 Tool만 바꾸면 내 서비스가 된다.

## ② 개념 설명

- 아이디어 캔버스 6칸: 사용자, 문제, 에이전트 역할, 도구, 화면, 위험.
- 템플릿 에이전트 `my_service_agent`: Instruction과 Tool을 교체한다. `agent.py`의 `TODO(1)~(3)`과 `tools.py`의 `TODO(1)`.
- 같은 AG-UI 서버(8000)와 CopilotKit 화면(3000)에 연결해 시연한다.

## ③ 아키텍처

PART 3의 구조와 같다. 바뀌는 것은 ADK 에이전트(`my_service_agent`)뿐이다. `labs/09-final-project/server.py`가 `labs/06-agui-backend/server.py`와 같은 8000번 포트, 같은 `/ag-ui` 경로를 쓰고 에이전트를 `doc_report_agent`라는 이름으로 등록하므로 Frontend는 고치지 않는다.

## ④ Hands-on

### L12 나만의 에이전트 프로토타입 (`labs/09-final-project`, 20분)

강의 중 진행(30분): 안내 3 → L12 20(설계 3 + 개발·연결 17) → 발표 4(희망 2팀, 팀당 2분) → 정리 3. Tool 하나를 만들어 화면에 연결하는 것이 목표다.

강의 뒤 이어 하기(확장판, 90분): 설계 10 → 개발 40 → UI 연결·테스트 20 → 발표 20(팀당 3분). 자세한 내용은 [최종 프로젝트 가이드](final-project-guide.md)에 있다.

```
adk web --port 8080 labs/09-final-project
```

목록에 `my_service_agent`가 보이고, 회의록에서 `extract_action_items`로 할 일을 찾아 응답하면 템플릿이 정상이다. 도구와 Instruction을 바꾼 뒤 화면에 연결한다. `labs/06-agui-backend`의 서버가 떠 있으면 먼저 끈다(같은 8000 포트).

```
python labs/09-final-project/server.py
```

```
npm --prefix labs/07-copilotkit-frontend run dev
```

http://localhost:3000 에서 대화한다. 확인:

```
python labs/09-final-project/check.py
```

흔한 실수: 도구의 docstring·타입 누락, 범위 과다, 실제 개인 정보 사용.

## ⑤ 실습 확장

**강의 뒤 과제**이다. 강의 시간(300분)에는 소개만 하고, 직접 해 보는 것은 강의가 끝난 뒤에 한다.

[해커톤 서비스 확장 가이드](../hackathon-extension-guide.md): 외부 API 도구, MCP 서버, 도구 전용 화면 카드.

## ⑥ 핵심 정리

- 아이디어 = 역할(Instruction) + 도구(Tool) + 화면(AG-UI).
- 시연 가능한 최소 범위(도구 1~2개, 화면 1개)부터.
- 시연 전 [보안·거버넌스 체크리스트](../security-checklist.md)를 훑는다.
