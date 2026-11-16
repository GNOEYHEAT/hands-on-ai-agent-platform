# L11 에이전트 보안 가드레일

이 실습(advanced 트랙의 실습 11)에서는 에이전트에 세 가지 가드레일을 붙이고, 저장소 보안 점검 스크립트를 실행합니다. 가드레일은 에이전트가 도구를 실행하기 전과 후에 입력과 결과를 검사해 위험한 동작을 막는 코드입니다. 이 실습의 가드레일은 허용 폴더 검사, 프롬프트 인젝션 탐지, 실행 로그 기록입니다.

## 구조

```
labs/08-security-governance/
├── audit.py                     SEC 자동 점검 항목 PASS/FAIL 출력
├── doc_report_agent/
│   ├── agent.py                 before_tool_callback, after_tool_callback 연결
│   ├── guardrails.py            가드레일 3종
│   ├── tools.py, mock_llm.py
└── check.py
```

콜백은 ADK가 정해진 시점에 대신 불러 주는 함수입니다. `before_tool_callback`은 도구 실행 직전에, `after_tool_callback`은 도구 실행 직후에 불립니다.

| 가드레일 | ADK 콜백 | 체크리스트 |
| --- | --- | --- |
| `block_outside_data` | `before_tool_callback` | SEC-05 data/ 밖 경로 거부 |
| `flag_prompt_injection` | `after_tool_callback`(`after_tool_guard` 안) | SEC-07 숨은 지시 탐지·경고 |
| `write_audit_log` | `after_tool_callback`(`after_tool_guard` 안) | SEC-08 `logs/agent_audit.jsonl` 기록, 키 가림 |

콜백이 `None`을 돌려주면 도구 실행이 그대로 진행됩니다. dict를 돌려주면 그 값이 도구 결과를 대신합니다.

## 실행

가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널에서, 저장소 최상위 폴더에 있는 상태로 진행합니다.

1. 보안 점검 스크립트를 실행하세요.

   ```
   python labs/08-security-governance/audit.py
   ```

2. 가드레일을 붙인 에이전트와 대화를 시작하세요.

   ```
   adk run labs/08-security-governance/doc_report_agent
   ```

`audit.py`의 출력은 다음과 같습니다. `수동`으로 표시된 항목은 스크립트로 검사할 수 없어 사람이 직접 확인해야 하는 항목입니다.

```
SEC-01 PASS  코드에 키 형태 문자열 없음, .env는 .gitignore
SEC-02 PASS  .env.example의 GOOGLE_API_KEY 값이 비어 있음
SEC-03 PASS  Frontend 코드에 키 없음(Backend 경유)
SEC-05 PASS  data/ 밖 경로 3건 거부, data/ 안 문서는 읽기 허용
SEC-07 PASS  injection_test.md에서 인젝션 패턴 2개 탐지
SEC-08 PASS  실행 로그의 키 값 가림 처리 확인
SEC-11 PASS  CORS 허용 출처 "http://localhost:3000"
SEC-04 수동  사용자를 식별·인증하고 사용자별 권한을 나눈다
...
자동 점검 7개 중 PASS 7개, FAIL 0개
```

`adk run`이 시작되면 다음 두 문장을 차례로 입력해 보세요.

1. `../.env 파일을 읽어 줘`를 입력하세요. 에이전트가 `보안 정책: data/ 폴더 밖 경로는 읽을 수 없습니다 (../.env)`라며 거부합니다.
2. `data/samples/injection_test.md 를 분석해 줘`를 입력하세요. 답의 맨 앞에 `경고: 문서에 에이전트 지시를 바꾸려는 문장(프롬프트 인젝션 의심)이 있습니다.`가 나옵니다. 프롬프트 인젝션은 문서나 입력에 숨긴 지시로 에이전트의 원래 지시를 무시하게 만드는 공격입니다. 에이전트는 문서 속 숨은 지시(.env 내용 적기)를 따르지 않습니다.
3. `exit`를 입력해 대화를 끝내세요.

그다음 편집기로 `logs/agent_audit.jsonl`을 열어 도구 호출 기록을 확인하세요.

```
{"time": "...", "user": "test_user", "tool": "read_document", "args": {"path": "../.env"}, "status": "error", "blocked": true, "warning": null}
{"time": "...", "user": "test_user", "tool": "read_document", "args": {"path": "data/samples/injection_test.md"}, "status": "success", "blocked": false, "warning": "문서에 에이전트 지시를 바꾸려는 문장(프롬프트 인젝션 의심)이 있습니다."}
```

`user`에는 `adk run`으로 대화했을 때 `test_user`가 남습니다. `check.py`로 확인했을 때는 `student`가 남습니다.

## 한계

- 인젝션 탐지는 정규식 패턴 목록으로 합니다. 정규식은 글자의 모양으로 문장을 찾는 규칙입니다. 그래서 표현을 바꾼 공격은 놓칠 수 있습니다. Instruction의 "문서는 데이터" 규칙, 도구 권한 최소화, 사람의 확인을 함께 쓰세요.
- 로그의 `user`는 ADK 세션의 사용자 ID입니다. 프로토타입에서는 고정값입니다. 실제 서비스에서는 로그인으로 확인한 사용자를 넣어야 합니다(SEC-04).

## 확인

저장소 최상위 폴더에서 다음 명령을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/08-security-governance/check.py
```
