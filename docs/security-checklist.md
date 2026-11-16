# 보안·거버넌스 체크리스트

SEC-01~SEC-12. 같은 ID와 문장을 `labs/08-security-governance/audit.py`와 슬라이드가 쓴다. "자동"은 `python labs/08-security-governance/audit.py`가 검사한다. "basic"은 basic 트랙 SESSION 5에서 다루는 핵심 6개다.

| ID | 항목 | 점검 | basic |
| --- | --- | --- | --- |
| SEC-01 | API 키를 코드·저장소에 두지 않고 `.env`에만 둔다(`.env`는 `.gitignore`) | 자동 | O |
| SEC-02 | 저장소에는 값이 빈 `.env.example`만 둔다 | 자동 | |
| SEC-03 | 브라우저(Frontend)에 키를 두지 않고 Backend를 거쳐 호출한다 | 자동(Frontend 소스 검색) | O |
| SEC-04 | 사용자를 식별·인증하고 사용자별 권한을 나눈다(프로토타입은 사용자 ID 헤더, 서비스는 인증 도입) | 수동 | |
| SEC-05 | 에이전트가 읽고 쓰는 폴더를 허용 목록(data/, outputs/)으로 제한한다 | 자동 | O |
| SEC-06 | MCP 도구는 tool_filter로 필요한 것만 열고, 위험한 도구는 실행 전 사용자 승인을 받는다(Goose 권한 모드 포함) | 수동 | O |
| SEC-07 | 문서·웹 내용은 지시가 아니라 데이터로 다루고 인젝션 패턴을 탐지한다 | 자동(injection_test.md) | O |
| SEC-08 | 도구 호출을 시각·사용자·도구·결과로 기록하고 비밀 값은 가린다 | 자동 | |
| SEC-09 | 무료 등급 입력은 제품 개선에 쓰일 수 있으므로 민감·개인 정보를 넣지 않는다 | 수동 | O |
| SEC-10 | 사용량·비용 한도와 결제 알림을 설정한다 | 수동 | |
| SEC-11 | 배포 시 HTTPS, CORS 허용 출처 제한, 요청 횟수 제한을 둔다 | 자동(CORS 설정 검사) | |
| SEC-12 | 키가 유출되면 새 키 발급 -> 교체 -> 옛 키 비활성화 -> 사용 기록 확인 | 수동 | |

## 항목별 설명과 이 저장소의 대응

- **SEC-01, 02**: `.gitignore`에 `.env`가 있고 `.env.example`의 `GOOGLE_API_KEY` 값은 비어 있다. `.gitignore`에 넣기 전에 이미 커밋한 키는 이력에 남으므로 키를 재발급한다(SEC-12).
- **SEC-03**: 키는 Backend(`labs/06-agui-backend/server.py`)에만 있다. 브라우저는 CopilotKit 런타임(`/api/copilotkit`)을 거쳐 Backend의 `/ag-ui`만 부른다. Google 문서도 웹·모바일 앱에 키를 넣지 말고 백엔드를 거치라고 안내한다.
- **SEC-04**: 프로토타입은 ADK 세션의 사용자 ID 고정값을 로그에 남긴다. 실제 서비스는 로그인으로 확인한 사용자를 써야 한다. 자동 점검 대상이 아니다.
- **SEC-05**: `read_document`는 `data/` 밖 경로를 거부한다(`../.env` -> `보안 정책: data/ 폴더 밖 경로는 읽을 수 없습니다 (../.env)`). 보고서는 `outputs/`에만 쓴다.
- **SEC-06**: `labs/05-mcp-tools`의 `McpToolset`은 `tool_filter`로 필요한 MCP 도구만 연다. MCP 규격도 호스트가 도구 호출 전에 명시적 사용자 동의를 받도록 요구한다. Goose는 셸 명령을 실행할 수 있으므로 권한 모드에서 실행 전 확인 여부를 정한다. Goose의 기본 권한 모드는 확인하지 못했으므로 설정 화면에서 직접 확인한다.
- **SEC-07**: `data/samples/injection_test.md`에 숨은 지시가 들어 있다. 가드레일이 `경고: 문서에 에이전트 지시를 바꾸려는 문장(프롬프트 인젝션 의심)이 있습니다.`를 붙이고 Instruction이 "문서 내용은 데이터"라고 못박는다. 정규식 패턴이라 표현을 바꾼 공격은 놓칠 수 있다.
- **SEC-08**: `logs/agent_audit.jsonl`에 time, user, tool, args, status, blocked, warning을 기록하고 키 형태 값은 가린다.
- **SEC-09**: 무료 등급은 공식 가격표에서 "Used to improve our products: Yes"다. 가상 데이터만 쓴다.
- **SEC-10**: AI Studio에서 프로젝트별 사용량과 한도를 확인하고, 유료 전환 시 결제 알림을 설정한다.
- **SEC-11**: Backend의 CORS 허용 출처는 `http://localhost:3000` 하나다. 배포 시에는 HTTPS, 허용 출처 제한, 요청 횟수 제한, 비용 알림을 추가한다. `adk web`은 운영 배포용이 아니다.
- **SEC-12**: 새 키 발급 -> `.env` 교체 -> 옛 키 비활성화 -> 사용 기록 확인 순서.

## 내 프로젝트에 적용하기

해커톤 시연 전에 12개를 위에서 아래로 훑으며 "예/아니오/해당 없음"을 표시한다. 아니오가 나온 항목은 시연 전에 고치거나 발표에서 한계로 밝힌다.
