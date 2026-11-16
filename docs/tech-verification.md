# 기술 검증 결과와 출처

확인 기준일: 2026-11-15. 공식 문서와 패키지 저장소에서 확인한 것만 적었다. 확인하지 못한 것은 맨 아래 "확인하지 못한 것"에 따로 모았다.

## 실행 환경

| 항목 | 선택 | 근거 |
| --- | --- | --- |
| OS | Windows, macOS | 요청. 명령은 두 OS에서 같게 쓴다(가상환경 활성화만 다름) |
| Python | 3.12 권장, 3.11~3.13 허용 | google-adk 2.14.1이 Python 3.11 이상 필요(PyPI). ADK 문서는 3.10 이상, ag-ui-adk는 3.10 이상 3.16 미만. 높은 쪽을 따랐다. 3.14는 확인하지 못해 제외 |
| Node.js | 22 LTS 이상 권장(최소 20.9) | Next.js 16.4.6은 20.9 이상, @copilotkit/runtime 1.88.0은 20 이상, ADK CopilotKit 문서는 18 이상 |
| 모델 | `gemini-3.5-flash-lite` | 아래 참고. `.env`의 `DOC_AGENT_MODEL`로 교체 |

### 확정한 버전

- Python(`requirements.txt`): google-genai 2.34.0, google-adk[mcp] 2.14.1, mcp 2.3.0, ag-ui-adk 0.13.0, ag-ui-protocol 1.0.0, fastapi 0.163.0, uvicorn[standard] 0.54.0, python-dotenv 1.2.4, httpx 0.28.1
- npm(`labs/07-copilotkit-frontend/package.json`): next 16.4.6, react·react-dom 19.3.1, @copilotkit/react-core 1.88.0, @copilotkit/runtime 1.88.0, @ag-ui/client 1.0.2(react-core·runtime이 의존하는 버전에 맞춤), hono 4.13.18, zod 3.25.76, typescript 5.9.3
- 개발 PC(Windows 11, Python 3.12.10, Node.js v24.18.0, npm 11.16.0)에서 `pip install`, `npm install`, `npm run build`가 성공했다.

## 확인한 사실과 출처

| 항목 | 확인 결과 | 출처 |
| --- | --- | --- |
| 모델 ID `gemini-3.5-flash-lite` | 사용 가능. 모델 페이지에 Stable로 표기, 최신 업데이트 2026년 7월. 입력 1,048,576 / 출력 65,536 토큰. Function calling·Thinking·Structured outputs 지원 | https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite |
| 무료 등급 | Standard 무료 등급 입출력 "Free of charge". 가격표의 Batch·Priority도 무료 등급 칸은 "Free of charge"이고 Flex만 "Not available"이다(이 강의는 Standard만 쓴다). 유료는 입력 $0.30/1M, 출력 $2.50/1M. 무료 등급은 "Used to improve our products: Yes" | https://aistudio.google.com/docs/pricing |
| 무료 등급 한도 | 문서에 Flash-Lite 무료 등급 한도 표가 없다. "rate limits can be viewed in Google AI Studio", "Specified rate limits are not guaranteed" | https://aistudio.google.com/docs/rate-limits , https://aistudio.google.com/rate-limit |
| 대체 모델 | `gemini-3.1-flash-lite`, `gemini-2.5-flash-lite` 모두 무료 등급 "Free of charge". 변경은 `.env`의 `DOC_AGENT_MODEL`(Goose는 Use custom model에 같은 ID) | https://aistudio.google.com/docs/pricing |
| API 키 환경 변수 | SDK는 `GEMINI_API_KEY` 또는 `GOOGLE_API_KEY`를 읽고 둘 다 있으면 `GOOGLE_API_KEY`가 우선. 키를 Git에 넣지 말고 웹·모바일 앱에 넣지 말고 백엔드를 거친다 | https://aistudio.google.com/docs/api-key |
| Interactions API | 2026년 6월 기준 GA이며 신규 프로젝트에 권장. 기존 `generateContent`도 계속 지원(레거시). Python은 google-genai 2.3.0 이상 | https://aistudio.google.com/docs/interactions-overview , https://aistudio.google.com/docs/quickstart |
| Goose 설치 | 저장소 https://github.com/aaif-goose/goose (AAIF). Windows setup.exe 또는 ZIP, macOS ZIP 또는 `brew install --cask block-goose`. 공식 시스템 요구 사항 표는 없음 | https://goose-docs.ai/docs/getting-started/installation |
| Goose의 Gemini 연결 | 프로바이더 표 이름은 Gemini, 실제 Desktop 화면(사용자 제공) 표기는 Google Gemini (API Key). 프로바이더 "Gemini", 필수 `GOOGLE_API_KEY`. Desktop: Settings → Models → Configure providers → 프로바이더 선택 → 키 입력 → Submit. 모델은 Switch models → Use custom model로 입력. CLI `goose configure`는 사용자 지정 모델 이름을 지원하지 않음 | https://goose-docs.ai/docs/getting-started/providers |
| Goose 실제 화면(사용자 제공) | 사용자가 제공한 실제 화면(2026-11-15 캡처)에서 Goose Desktop에 Google Gemini (API Key) 프로바이더를 연결하고 gemini-3.5-flash-lite로 한국어 대화가 되는 것을 확인했다. 첫 실행 화면에서 "제공업체에 연결" → "Google Gemini (API Key)" → "Google API Key" 입력 → "계속"이며, 화면에 "키는 키체인에 안전하게 저장됩니다"라고 나온다. 하네스가 직접 실행해 확인한 것이 아니라 사용자 제공 화면 기준이다. 모델을 고르는 화면의 캡처는 없다 | slides/assets/goose-1-welcome.png ~ goose-4-chat.png |
| Goose 로컬 파일·코드 | Developer 확장이 파일 편집·셸 명령을 맡고 설치 시 기본 활성. `.goosehints`로 맥락 제공 | https://goose-docs.ai/docs/mcp/developer-mcp , https://goose-docs.ai/docs/guides/context-engineering/using-goosehints (검색 결과 요약으로만 확인) |
| ADK 설치·실행 | `pip install google-adk`, 에이전트 폴더 = `agent.py`·`__init__.py`, `root_agent`, `adk run`, `adk web`. "ADK Web is not meant for use in production deployments." | https://adk.dev/get-started/python/ |
| ADK 버전 | PyPI google-adk 2.14.1(2026-11-12), `requires_python >=3.11` | https://pypi.org/project/google-adk/ |
| ADK MCP | `pip install "google-adk[mcp]"`, `McpToolset`, `StdioConnectionParams`, `tool_filter` 권장 | https://adk.dev/tools-custom/mcp-tools/ |
| MCP 규격 | 최신 규격 2026-07-28. JSON-RPC 2.0, Hosts·Clients·Servers, Tools·Resources·Prompts. "Hosts must obtain explicit user consent before invoking any tool" | https://modelcontextprotocol.io/specification/latest |
| ADK–AG-UI 공식 지원 | 지원됨. AG-UI 문서의 프레임워크 표에 Google ADK가 "1st Party"로 Supported. ADK 문서에 AG-UI·CopilotKit 연동 페이지가 있다 | https://docs.ag-ui.com/introduction , https://adk.dev/integrations/ag-ui/ , https://adk.dev/integrations/copilotkit/ |
| ag-ui-adk | PyPI 0.13.0, import `ag_ui_adk`, `ADKAgent`, `add_adk_fastapi_endpoint` | https://pypi.org/project/ag-ui-adk/ |
| CopilotKit과 AG-UI의 관계 | AG-UI는 에이전트와 사용자 앱을 잇는 오픈 이벤트 기반 프로토콜이고 CopilotKit과 LangChain·CrewAI의 협력에서 출발했다. CopilotKit은 ADK 에이전트와 앱을 잇는 오픈소스 프레임워크로 AG-UI 엔드포인트에 채팅, 스트리밍, 생성형 UI, 공유 상태, HITL을 제공한다. 정리: AG-UI = 프로토콜, CopilotKit = 그 프로토콜의 대표 프론트엔드 구현 | https://docs.ag-ui.com/introduction , https://docs.copilotkit.ai/adk |
| AG-UI·MCP·A2A | AG-UI(에이전트↔사용자), MCP(에이전트↔도구·데이터), A2A(에이전트↔에이전트) | https://docs.ag-ui.com/introduction |
| AG-UI 이벤트 | Lifecycle, Text Message, Tool Call, State 등 | https://docs.ag-ui.com/concepts/events |
| CopilotKit·Next.js | `@copilotkit/react-core` 1.88.0, `@copilotkit/runtime` 1.88.0, next 16.4.6 | https://www.npmjs.com/package/@copilotkit/react-core , https://www.npmjs.com/package/@copilotkit/runtime , https://www.npmjs.com/package/next |

## 설치로 확정한 것 (설계 시 미확인이던 항목)

- 이벤트 `type`의 실제 전송 값은 `RUN_STARTED`처럼 대문자 스네이크 케이스다.
- CopilotKit 1.88.0의 `@copilotkit/runtime/v2`는 `CopilotRuntime`, `createCopilotRuntimeHandler`, `createCopilotEndpoint`를 모두 export한다. 이 실습은 Next.js에 맞는 `createCopilotRuntimeHandler`를 쓴다.
- mcp 2.3.0의 서버 클래스는 `MCPServer`(예전 `FastMCP`는 이름이 바뀌어 import하면 실패).
- 모의 모델은 ag-ui-adk와 CopilotKit 런타임을 거쳐 화면까지 동작한다.
- `adk run`/`adk web`은 에이전트 폴더에서 상위로 올라가며 `.env`를 찾는다. 그래서 저장소 최상위 `.env`가 읽힌다. 단 Next.js는 최상위 `.env`를 읽지 않는다.

## 확인하지 못한 것

1. **이 저장소 코드의 실제 Gemini 호출**: 개발 환경에 API 키가 없어 `gemini-3.5-flash-lite`를 Interactions API와 `generateContent`로 호출하는 것, 모델 목록에 이 ID가 나오는지, 실제 모델이 도구를 제대로 고르는지, 실제 모델의 AG-UI 이벤트 순서, 429·404 메시지가 실제로 나오는지는 확인하지 못했다. 문서의 Interactions API 예제는 다른 모델 ID를 쓴다. 키가 있으면 `python labs/01-gemini-api/check.py --live`로 확인할 수 있다.
2. **무료 등급 한도 수치**(RPM·TPM·RPD): 공식 문서에 표가 없다. 수치를 적지 않았다.
3. **한국에서의 무료 등급 이용 가능 여부**: 확인하지 않았다.
4. **Goose Desktop**: 사용자 제공 화면으로 프로바이더 연결과 한국어 대화는 확인했다(위 표). 여전히 확인하지 못한 것은 모델을 고르는 화면의 모습, 모델 목록에 `gemini-3.5-flash-lite`가 기본으로 보이는지, 공식 문서의 Settings 경로가 현재 화면과 같은지, 기본 권한 모드, Goose로 `doc_stats.py`를 만드는 실습 과정이다.
5. **Python 3.14 호환**: 확인하지 못해 제외했다.
6. 브라우저 화면은 자동화된 브라우저로만 확인했고 사람이 입력해 보지 않았다. macOS는 확인하지 못했다.
7. Goose의 일부 문서(Developer 확장, `.goosehints`)와 Gemini 3.6 Flash·3.5 Flash-Lite GA 발표 글(https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)은 검색 결과 요약으로만 확인했다.
