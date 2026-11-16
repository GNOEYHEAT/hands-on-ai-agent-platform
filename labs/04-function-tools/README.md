# L2·L7 문서 분석 Function Tool

이 실습에서는 에이전트에 `read_document`, `analyze_document`, `save_report` 세 가지 Function Tool을 붙입니다. Function Tool은 타입 힌트와 docstring(함수 설명 글)을 가진 Python 함수를 에이전트가 부를 수 있는 도구로 등록한 것입니다. 에이전트는 이 도구로 파일을 읽고, 분석하고, 보고서를 저장합니다.

- L2는 basic 트랙의 실습 2입니다. `adk web`으로 실행합니다.
- L7은 advanced 트랙의 실습 7입니다. `adk run`과 `adk web` 모두로 실행합니다.

## 구조

```
labs/04-function-tools/
├── doc_report_agent/
│   ├── agent.py      root_agent에 tools=[read_document, analyze_document, save_report]
│   ├── tools.py      세 도구. 타입 힌트와 docstring은 모델에게 주는 도구 설명으로 쓰임
│   └── mock_llm.py   모의 모델
└── check.py
```

| 도구 | 하는 일 |
| --- | --- |
| `read_document(path)` | `data/` 기준 상대 경로(예: `samples/project_status_report.md`)의 .md/.txt 파일을 읽습니다. `data/` 밖의 파일은 거부합니다 |
| `analyze_document(text)` | 제목, 소제목, 핵심 항목, 문제점(위험·지연·TODO 등)을 정해진 규칙으로 뽑습니다 |
| `save_report(title, markdown)` | `outputs/`에 `날짜-시각_제목.md`로 저장하고 저장 경로를 돌려줍니다 |

## 실행

가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널에서, 저장소 최상위 폴더에 있는 상태로 진행합니다.

1. 터미널에서 대화하려면 다음 명령을 실행하세요.

   ```
   adk run labs/04-function-tools/doc_report_agent
   ```

2. 브라우저 화면으로 대화하려면 다음 명령을 실행하세요. `adk web`은 ADK의 개발 UI(에이전트를 브라우저에서 시험해 보는 개발용 화면)를 띄우는 명령입니다. 서버가 켜져 있는 동안 이 터미널은 그대로 두세요.

   ```
   adk web --port 8080 labs/04-function-tools
   ```

3. 브라우저 주소창에 http://localhost:8080 을 입력하세요. 8080은 이 화면이 쓰는 포트 번호입니다. 포트는 한 컴퓨터 안에서 여러 프로그램이 통신 창구를 나눠 쓰도록 붙이는 번호입니다.
4. 왼쪽 위에서 `doc_report_agent`를 고르세요.
5. `샘플 보고서를 분석해 줘`라고 입력하세요.
6. 이벤트(Events) 패널에서 `read_document` → `analyze_document` → `save_report` 호출과 결과를 확인하세요.

개발 UI는 개발용입니다. 서비스 배포에는 쓰지 마세요.

모의 모델(`DOC_AGENT_MODEL=mock`)로 실행했을 때 답의 앞부분은 다음과 같습니다.

```
(모의 모델 응답)

## 요약
'스마트 배송 앱 프로젝트 주간 현황 보고' 문서를 분석했습니다. 핵심 항목 5개, 문제점 6개를 찾았습니다.
...
보고서를 outputs/20261115-171435_스마트_배송_앱_프로젝트_주간_현황_보고.md에 저장했습니다.
```

## 해 볼 것

- `tools.py`의 `ISSUE_KEYWORDS`에 단어를 추가하고 `customer_feedback.txt`를 분석해 보세요.
- docstring을 지우거나 바꿨을 때 실제 모델이 도구를 어떻게 고르는지 비교해 보세요(API 키가 필요합니다).

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/04-function-tools/check.py
```

## 막히면

| 화면에 보이는 것 | 원인과 해결 |
| --- | --- |
| 8080 포트를 이미 쓰고 있다는 오류 | 다른 프로그램이 8080 포트를 쓰고 있습니다. `adk web --port 8081 labs/04-function-tools`처럼 다른 포트를 쓰세요 |
| `adk web`에 에이전트가 보이지 않음 | `labs/04-function-tools/doc_report_agent`가 아니라 부모 폴더 `labs/04-function-tools`를 주어야 합니다 |
