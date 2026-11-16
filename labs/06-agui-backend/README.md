# L9 ADK 에이전트를 AG-UI로 노출

이 실습(advanced 트랙의 실습 9)에서는 `ag-ui-adk` 패키지로 `doc_report_agent`(L7과 같은 Function Tool 버전)를 http://localhost:8000/ag-ui 엔드포인트로 엽니다. 그리고 에이전트가 보내는 이벤트를 직접 관찰합니다.

- AG-UI는 에이전트(Backend, 에이전트가 실행되는 서버)와 화면(Frontend)이 주고받는 메시지의 형식과 순서를 정한 약속(프로토콜)입니다. 화면이 실행 요청을 보내면, Backend가 실행 과정을 이벤트로 차례로 돌려보냅니다.
- 엔드포인트는 서버에서 요청을 받는 주소입니다. 여기서는 `/ag-ui`입니다.
- `ag-ui-adk`는 ADK 에이전트를 AG-UI 엔드포인트로 열어 주는 Python 패키지입니다.

## 구조

```
labs/06-agui-backend/
├── server.py          FastAPI + ADKAgent + add_adk_fastapi_endpoint(app, agent, path="/ag-ui"), 포트 8000
├── send_run.py        RunAgentInput을 POST하고 SSE 이벤트 type을 한 줄씩 출력
├── doc_report_agent/  L7과 같은 에이전트
└── check.py
```

SSE(Server-Sent Events)는 서버가 연결을 열어 둔 채 이벤트를 차례로 보내 주는 방식입니다.

## 실행

이 실습에는 터미널이 2개 필요합니다. 두 터미널 모두 가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널이어야 하고, 저장소 최상위 폴더에서 진행합니다.

1. 터미널 1에서 Backend 서버를 띄우세요. 이 터미널은 끄지 말고 그대로 두세요.

   ```
   python labs/06-agui-backend/server.py
   ```

2. 터미널 2를 새로 열고 요청을 보내세요.

   ```
   python labs/06-agui-backend/send_run.py
   ```

모의 모델(`DOC_AGENT_MODEL=mock`)로 실행했을 때의 출력입니다(긴 줄은 줄였습니다).

```
RUN_STARTED
TOOL_CALL_START        read_document
TOOL_CALL_ARGS         {"path":"samples/project_status_report.md"}
TOOL_CALL_END
TOOL_CALL_RESULT
TOOL_CALL_START        analyze_document
...
TOOL_CALL_START        save_report
...
TEXT_MESSAGE_START
TEXT_MESSAGE_CONTENT   (모의 모델 응답)  ## 요약 '스마트 배송 앱 프로젝트 주간 현황 보
TEXT_MESSAGE_CONTENT   고' 문서를 분석했습니다. 핵심 항목 5개, 문제점 6개를 찾았습니다.
...
TEXT_MESSAGE_END
STATE_SNAPSHOT
RUN_FINISHED
```

- `TEXT_MESSAGE_CONTENT`가 여러 번 오는 것이 스트리밍입니다. 화면은 이 조각을 이어 붙여 글자가 흘러나오듯 보여 줍니다.
- 실제 Gemini는 도구를 부르기 전에 짧은 문장을 먼저 말할 수 있습니다. 그래서 `TEXT_MESSAGE_*`가 `TOOL_CALL_*`보다 먼저 나올 수도 있습니다. 순서는 모델의 판단에 따라 달라집니다.
- 다른 문서로 해 보려면 터미널 2에서 다음 명령을 실행하세요: `python labs/06-agui-backend/send_run.py --message "data/samples/meeting_notes.md 를 분석해 줘"`

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/06-agui-backend/check.py
```

`check.py`는 비어 있는 포트에 모의 모델로 서버를 직접 띄우고, 이벤트 순서를 확인한 뒤 서버를 끕니다. 그래서 터미널 1의 서버가 켜져 있어도 실행할 수 있습니다.

## 막히면

| 화면에 보이는 것 | 원인과 해결 |
| --- | --- |
| `[Errno 10048]` 또는 `address already in use` | 8000 포트를 다른 프로그램(또는 L12 서버)이 쓰고 있습니다. 그 프로그램을 끄거나, 터미널 1에서 `PORT` 환경 변수를 8001처럼 다른 번호로 정한 뒤 서버를 다시 띄우세요. 환경 변수를 정하는 방법은 최상위 README의 [터미널에서 환경 변수를 잠깐 정하는 법](../../README.md#터미널에서-환경-변수를-잠깐-정하는-법)에 있습니다. 포트를 바꿨다면 터미널 2의 `send_run.py`에도 `--url`로 바뀐 주소를 알려 주세요. 예: `python labs/06-agui-backend/send_run.py --url http://localhost:8001/ag-ui`. 알려 주지 않으면 기본 주소(8000번)로 연결하려다 서버를 먼저 실행하라는 안내가 나옵니다. Frontend를 쓸 때는 `ADK_AG_UI_URL`도 같은 주소로 바꿔야 합니다 |
| `send_run.py`가 연결하지 못했다는 메시지 | 터미널 1의 서버가 켜져 있는지 확인하세요 |
