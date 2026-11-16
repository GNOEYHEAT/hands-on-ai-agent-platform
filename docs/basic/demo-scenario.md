# basic 최종 데모 시나리오

SESSION 4의 마지막 3.5분. 브라우저에서 문서 분석 에이전트와 대화하는 장면을 보여 준다. 아래 입력과 기대 화면은 모의 모델로 실제 확인한 결과이며, 실제 Gemini 모델로는 확인하지 못했다.

## 사전 상태

- 터미널 1: `python labs/06-agui-backend/server.py` 실행 중(8000)
- 터미널 2: `npm --prefix labs/07-copilotkit-frontend run dev` 실행 중(3000)
- 브라우저: http://localhost:3000
- 가상환경 활성화, `.env` 작성 완료. 키 없이 시연하려면 `.env`에 `DOC_AGENT_MODEL=mock`

## 시나리오

| 단계 | 입력/동작 | 기대 화면 |
| --- | --- | --- |
| 1 | `샘플 보고서를 분석해 줘` 입력 | 답이 조각 단위로 흘러나온다(스트리밍) |
| 2 | 도구 상태 카드를 가리킨다 | `read_document` 완료, `analyze_document 완료 핵심 항목 5개, 문제점 6개`, `save_report 완료 저장: outputs/...md` |
| 3 | 오른쪽 패널을 가리킨다 | '보고서 결과' 패널에 제목·핵심 항목·문제점·저장 경로 |
| 4 | `data/samples/meeting_notes.md` 전체를 붙여 넣는다 | `analyze_document 완료 핵심 항목 5개, 문제점 3개`, `save_report 완료`, 패널 갱신 |

말할 것: "화면 왼쪽 글자는 AG-UI의 `TEXT_MESSAGE_CONTENT` 이벤트, 카드는 `TOOL_CALL_*` 이벤트가 만든다. 키는 Backend에만 있고 브라우저에는 없다."

## 실패 시 대체 경로

| 상황 | 대체 |
| --- | --- |
| 답이 오지 않는다 | Backend가 꺼져 있다. 터미널 1을 확인하고 다시 띄운다 |
| 8000 포트 충돌 (`[Errno 10048]`) | 8000을 쓰는 프로그램(다른 `server.py`)을 끈다 |
| 3000 포트 충돌 | `npm --prefix labs/07-copilotkit-frontend run dev -- --port 3001`, 주소를 3001로 |
| 429 (무료 한도) | `.env`의 `DOC_AGENT_MODEL=mock`으로 바꾸고 Backend를 다시 띄운다 |
| 화면 자체가 안 뜬다 | `python labs/07-copilotkit-frontend/check.py`로 Backend 왕복까지 확인해 터미널 출력으로 시연한다. 그래도 안 되면 `python labs/06-agui-backend/send_run.py`로 이벤트 스트림을 보여 준다 |
| 시간이 부족하다 | 참가자 실습(L3)을 건너뛰고 이 시연만 한다 |

## 시연 전 점검(5분 전)

```
python labs/07-copilotkit-frontend/check.py
```

`CHECK OK`가 나오면 Backend 왕복과 정적 설정이 맞는 것이다. 개발 서버 로그의 `[CopilotKit] Listing and clearing threads need a caller identity...` 경고는 무시해도 된다.
