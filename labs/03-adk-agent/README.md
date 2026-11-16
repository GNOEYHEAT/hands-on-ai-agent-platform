# L6 첫 ADK 에이전트

이 실습(advanced 트랙의 실습 6)에서는 Model과 Instruction만 가진 첫 에이전트 `doc_report_agent`를 만들어 `adk run`으로 대화합니다. Google ADK(이후 "ADK")는 에이전트를 코드로 정의하고 실행하게 해 주는 Google의 프레임워크입니다. Instruction은 에이전트의 역할과 답변 규칙을 적은 지시문입니다.

## 구조

```
labs/03-adk-agent/
├── doc_report_agent/      에이전트 폴더(adk run에 줄 폴더)
│   ├── __init__.py        from . import agent
│   ├── agent.py           root_agent = Agent(name, model, instruction)
│   └── mock_llm.py        키 없이 돌리는 모의 모델(DOC_AGENT_MODEL=mock)
└── check.py
```

`root_agent`는 ADK가 `agent.py`에서 찾는 진입 에이전트의 변수 이름입니다. 이 이름을 바꾸면 ADK가 에이전트를 찾지 못합니다.

## 실행

가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널에서, 저장소 최상위 폴더에 있는 상태로 진행합니다.

1. 에이전트와 대화를 시작하세요.

   ```
   adk run labs/03-adk-agent/doc_report_agent
   ```

2. `[user]:` 프롬프트가 나오면 `data/samples/meeting_notes.md`의 내용을 붙여 넣으세요. 에이전트가 요약, 핵심 항목, 문제점, 보고서 순서로 답합니다.
3. 대화를 끝내려면 `exit`를 입력하세요.

처음 실행하면 ADK가 `Enable telemetry? [Y/n]`을 물을 수 있습니다. 사용 통계를 보낼지 묻는 질문이고, 기본값은 꺼짐입니다.

질문 한 번으로 끝내려면 메시지를 명령 뒤에 함께 적으세요.

```
adk run labs/03-adk-agent/doc_report_agent "다음 회의록을 정리해 줘: ..."
```

## 해 볼 것

1. `agent.py`의 `INSTRUCTION`에서 답변 형식(요약, 핵심 항목, 문제점, 보고서)이나 말투를 바꾸세요. 다시 실행해 결과가 어떻게 달라지는지 비교해 보세요.
2. `.env`의 `DOC_AGENT_MODEL`을 `mock`으로 바꾸면 키 없이 같은 흐름을 볼 수 있습니다. 모의 모델은 API를 부르지 않고 미리 정한 규칙으로 답하는 테스트용 모델입니다. 글머리 항목을 뽑아 정해진 형식으로만 답합니다.

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/03-adk-agent/check.py
```

## 막히면

| 화면에 보이는 것 | 원인과 해결 |
| --- | --- |
| `adk: command not found` | 가상환경이 활성화되어 있지 않습니다. 가상환경을 활성화한 뒤 다시 실행하세요 |
| `No root_agent found` | `agent.py`의 변수 이름 `root_agent`를 바꿨거나, 폴더 대신 파일 경로(`agent.py`)를 주었습니다. 폴더 경로를 주세요 |
