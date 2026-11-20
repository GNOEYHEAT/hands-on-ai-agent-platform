# 최종 프로젝트 가이드

PART 5. 각자(또는 1~3인 팀)의 서비스 아이디어를 AI 에이전트 프로토타입으로 만들어 시연한다. 코드는 `labs/09-final-project`, 실습 상세는 `labs/09-final-project/README.md`.

## 강의 중 진행 (30분)

300분 강의의 마지막 30분(14:30~15:00)이다. 안내 3분 → L12 20분(설계 3 + 개발·연결 17) → 발표 4분 → 정리 3분으로 진행한다. 20분 안에서는 Tool 하나만 만들어 화면에 연결하는 것이 목표다.

| 단계 | 분 | 할 일 |
| --- | --- | --- |
| 안내 | 3 | 진행 방법과 평가 기준 확인 |
| 설계 | 3 | `labs/09-final-project/idea_canvas.md`의 6칸 중 역할(3번)·도구(4번)·화면(5번) 세 칸만 채운다 |
| 개발·연결 | 17 | `tools.py`에 Tool 하나를 만들고 `agent.py`의 TODO를 고친 뒤, `python labs/09-final-project/server.py`와 `npm --prefix labs/07-copilotkit-frontend run dev`로 화면에서 대화한다 |
| 발표 | 4 | 희망하는 2팀이 2분씩 |
| 정리 | 3 | 핵심 정리, 마무리 |

## 강의 뒤 이어 하기 (확장판, 90분)

강의 시간 안에 다 하지 못한 부분은 강의가 끝난 뒤 아래 순서로 이어서 한다.

| 단계 | 분 | 할 일 |
| --- | --- | --- |
| 설계 | 10 | `labs/09-final-project/idea_canvas.md`의 6칸을 채운다 |
| 개발 | 40 | `tools.py`에 도구를 만들고 `agent.py`의 TODO를 고친다. `adk web --port 8080 labs/09-final-project`로 시험 |
| UI 연결·테스트 | 20 | `python labs/09-final-project/server.py`와 `npm --prefix labs/07-copilotkit-frontend run dev`로 화면에서 대화 |
| 발표 | 20 | 팀당 3분 |

## 아이디어 캔버스 6칸

| 칸 | 질문 |
| --- | --- |
| 사용자 | 누가 쓰는가 |
| 문제 | 어떤 불편을 해결하는가 |
| 에이전트 역할 | 무엇을 하고 어떻게 답하는가(Instruction) |
| 도구 | 어떤 기능이 필요한가(Tool, 1~2개로 시작) |
| 화면 | 사용자가 무엇을 보는가(AG-UI) |
| 위험 | 틀리거나 오용될 때 무엇이 문제인가([체크리스트](../security-checklist.md)) |

## 고칠 곳

- `labs/09-final-project/my_service_agent/tools.py`: TODO(1) 예시 도구 `extract_action_items`를 내 도구로 바꾼다. 타입 힌트와 docstring을 쓴다.
- `labs/09-final-project/my_service_agent/agent.py`: TODO(1) `tools=[...]`, TODO(2) Instruction, TODO(3) 한 줄 소개.
- Frontend(`labs/07-copilotkit-frontend`)는 고치지 않는다. 새 도구는 `"*"` 카드로 실행 상태가 표시된다.

## 연결할 때 주의

- `labs/06-agui-backend`의 서버가 떠 있으면 먼저 끈다. `labs/09-final-project/server.py`도 8000번 포트를 쓴다.
- 화면은 에이전트를 `doc_report_agent`라는 이름으로 부르지만 실제로 답하는 것은 `my_service_agent`이다. `AGENT_ID`를 바꾸지 않는다.
- `python labs/09-final-project/check.py`를 도구를 바꾼 뒤에도 통과시킨다.

## 평가 기준 (제안)

이 기준은 이 강의에서 제안하는 것으로 코드가 검사하지는 않는다.

| 항목 | 보는 것 |
| --- | --- |
| 문제 정의 | 사용자와 문제가 한 문장으로 설명되는가 |
| 에이전트 설계 | 역할, 도구가 문제에 맞는가. 도구에 docstring·타입이 있는가 |
| 동작 | 화면에서 대화와 도구 상태가 보이는가. `check.py`를 통과하는가 |
| 보안 | 가상 데이터, 키 보호, 읽기·쓰기 범위 제한([체크리스트](../security-checklist.md)) |
| 발표 | 2~3분 안에 문제 → 시연 → 한계를 전달하는가 |

## 발표 형식(강의 중 2분, 확장판 3분)

강의 중에는 희망하는 2팀이 팀당 2분씩 발표한다. 순서는 문제와 사용자(20초), 에이전트 설계(40초), 시연(40초), 위험과 다음 단계(20초)다. 아래는 강의 뒤 확장판(팀당 3분)의 형식이다.

1. 문제와 사용자 (30초)
2. 에이전트 설계(역할·도구·화면) (60초)
3. 시연: 입력 한 번, 도구 상태, 결과 (60초)
4. 위험과 다음 단계 (30초)

키 없이도 시연할 수 있도록 모의 모델(`DOC_AGENT_MODEL=mock`) 대체 경로를 준비한다. 모의 모델은 새 도구를 사용자 메시지를 첫 인자로 넣어 한 번 호출한다.
