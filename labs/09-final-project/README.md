# L12 나만의 에이전트 프로토타입

이 실습(advanced 트랙의 실습 12)에서는 템플릿 에이전트 `my_service_agent`의 Instruction과 Tool을 내 아이디어로 바꿉니다. 그리고 L10에서 만든 CopilotKit 화면에 연결해 시연합니다. 템플릿은 그대로 실행되는 뼈대 코드이고, 바꿀 곳에 `TODO` 표시가 있습니다.

## 구조

```
labs/09-final-project/
├── idea_canvas.md          아이디어 캔버스(가장 먼저 채울 파일)
├── my_service_agent/
│   ├── agent.py            TODO(1)~(3): 도구 목록, Instruction, 한 줄 소개
│   ├── tools.py            TODO(1): 내 도구로 바꿀 예시 도구 extract_action_items
│   └── mock_llm.py         모의 모델(새 도구도 사용자 메시지를 첫 인자로 넣어 한 번 호출)
├── server.py               AG-UI 서버(포트 8000, 경로 /ag-ui)
└── check.py
```

템플릿 상태로도 동작합니다. 회의록을 붙여 넣으면 `extract_action_items`로 할 일을 찾아 정리합니다.

## 진행(90분)

1. 설계(10분): `idea_canvas.md`의 6칸을 채우세요.
2. 개발(40분): `tools.py`에 도구를 만들고 `agent.py`의 TODO를 고치세요. 그다음 `adk web`으로 시험하세요.
3. 화면 연결과 테스트(20분): `server.py`를 띄우고 L10 화면에서 대화해 보세요.
4. 발표(20분): 팀마다 3분씩 발표합니다.

## 실행

가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널에서, 저장소 최상위 폴더에 있는 상태로 진행합니다.

### 개발 중 시험하기(ADK 개발 UI)

1. 다음 명령으로 개발 UI를 띄우세요. 서버가 켜져 있는 동안 이 터미널은 그대로 두세요.

   ```
   adk web --port 8080 labs/09-final-project
   ```

2. 브라우저 주소창에 http://localhost:8080 을 입력하고 `my_service_agent`를 고른 뒤 대화하세요.

### 채팅 화면에 연결하기(터미널 2개)

L9의 `labs/06-agui-backend/server.py`가 켜져 있으면 먼저 끄세요. 같은 8000 포트를 쓰기 때문입니다.

1. 터미널 1에서 내 에이전트의 서버를 띄우세요. 이 터미널은 그대로 두세요.

   ```
   python labs/09-final-project/server.py
   ```

2. 터미널 2를 새로 열고 Frontend를 띄우세요. 이 터미널도 그대로 두세요.

   ```
   npm --prefix labs/07-copilotkit-frontend run dev
   ```

3. 브라우저 주소창에 http://localhost:3000 을 입력하고 대화하세요.

Frontend 코드는 고치지 않습니다. 화면은 이 서버의 에이전트를 `doc_report_agent`라는 이름으로 부르지만, 실제로 답하는 것은 `my_service_agent`입니다. 새로 만든 도구의 실행 상태는 Frontend의 `"*"` 카드로 표시됩니다.

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/09-final-project/check.py
```

`check.py`는 세 가지를 확인합니다. 도구마다 docstring이 있는지, 모의 모델로 도구를 부르고 답하는지, `server.py`가 AG-UI 이벤트(RUN_STARTED … RUN_FINISHED)를 보내는지입니다. 도구를 바꾼 뒤에도 이 검사를 통과해야 합니다.

## 흔한 실수

- 도구에 docstring이나 타입을 빼먹으면 모델이 도구를 고르지 못합니다. 둘 다 꼭 적으세요.
- 범위를 크게 잡으면 시간 안에 끝내기 어렵습니다. 도구 1~2개, 화면 1개로 시연할 수 있는 것부터 만드세요.
- 실제 고객 데이터나 개인 정보를 넣지 마세요. 가상 데이터만 쓰세요(SEC-09).
