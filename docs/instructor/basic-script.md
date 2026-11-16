# 강사용 발표 스크립트 — basic(60분)

- 슬라이드: `slides/hands-on-ai-agent-platform-basic.pptx` (원본 `slides/src/basic/slides.json`)
- 같은 스크립트가 슬라이드의 발표자 노트에도 들어 있다. 이 문서는 slides.json에서 만들었으므로 슬라이드를 고치면 함께 다시 만든다.
- 기술 사실의 출처와 확인하지 못한 항목은 `docs/tech-verification.md`에 있다. 화면 캡처는 사용자가 제공한 실제 화면(2026-11-15, slides/assets/의 8개, 키·개인 정보 가림)만 썼다. 캡처가 없는 화면(Goose 모델 선택, CopilotKit 채팅 등)은 구성도로 그리고 라이브로 보여 준다. 예상 시간 0분은 발표 시간 외(basic 부록).

총 28장, 슬라이드 예상 시간 합계 60분

## 한눈에 보기

| # | 모듈 | 제목 | 레이아웃 | 분 |
| --- | --- | --- | --- | --- |
| 1 | M1 | AI 에이전트 플랫폼 개발 Hands-on | title | 0.5 |
| 2 | M1 | 강의 전에 다섯 가지를 끝내 둔다 | table | 0.5 |
| 3 | M1 | 60분 동안 다섯 단계를 지난다 | agenda | 0.5 |
| 4 | M1 | SESSION 1. AI 에이전트 플랫폼의 이해 | section | 0.5 |
| 5 | M1 | LLM은 답하고, 에이전트는 도구로 일한다 | two_column | 1.5 |
| 6 | M1 | 오늘 만들 에이전트는 네 층으로 연결된다 | graph | 1.5 |
| 7 | M2 | SESSION 2. Gemini API 연결 및 Goose 활용 | section | 0.5 |
| 8 | M2 | 키 하나, 모델 ID 하나로 Gemini를 부른다 | flow | 2 |
| 9 | M2 | 실습 L1: Gemini API 연결 확인 | handson | 4 |
| 10 | M2 | Goose는 같은 키로 코드를 대신 만든다 | cards | 3.5 |
| 11 | M3 | SESSION 3. AI 에이전트 개발 | section | 0.5 |
| 12 | M3 | 에이전트 = Model + Instruction + Tool | cards | 3 |
| 13 | M3 | root_agent 하나가 에이전트 전체다 | code | 3.5 |
| 14 | M3 | 실습 L2: ADK 문서 분석 에이전트 실행 | handson | 8 |
| 15 | M4 | SESSION 4. AG-UI를 활용한 채팅 화면 구현 | section | 0.5 |
| 16 | M4 | AG-UI 이벤트가 화면을 만든다 | flow | 4 |
| 17 | M4 | 실습 L3: 브라우저 채팅 화면 연결 | handson | 12 |
| 18 | M4 | 최종 시연: 채팅과 보고서 패널이 함께 움직인다 | two_column | 3.5 |
| 19 | M5 | SESSION 5. 보안 및 해커톤 프로젝트 적용 | section | 0.5 |
| 20 | M5 | 보안 체크리스트 핵심 여섯 가지 | table | 4 |
| 21 | M5 | 내 아이디어는 역할·도구·화면 세 칸으로 옮긴다 | cards | 5.5 |
| 22 | - | 부록: 사전 준비 화면 | section | 0 |
| 23 | - | 'API 키 만들기'를 누른다 | image | 0 |
| 24 | - | 키 이름과 프로젝트를 정하고 '키 만들기'를 누른다 | image | 0 |
| 25 | - | '키 복사'로 복사해 .env에만 붙여 넣는다 | image | 0 |
| 26 | - | Goose 첫 화면에서 '제공업체에 연결'을 누른다 | image | 0 |
| 27 | - | Google Gemini (API Key)를 고르고 키를 넣는다 | image | 0 |
| 28 | - | 한국어로 말을 걸어 답이 오면 연결 끝 | image | 0 |

## SESSION 1. AI 에이전트 플랫폼의 이해

### 1. AI 에이전트 플랫폼 개발 Hands-on

- 핵심 메시지: AI 모델을 직접 만들지 않아도 API로 나만의 AI 에이전트 서비스를 만들 수 있다
- 예상 시간: 0.5분
- 시각 자료: 표지 (`title`)
- 본문 요약: basic · 60분 핵심 요약 — Gemini API, Goose, Google ADK, AG-UI, CopilotKit

스크립트:

> 안녕하세요. 오늘 60분 동안 문서 분석 및 보고서 작성 AI 에이전트 하나를 따라가며, 모델 연결부터 브라우저 채팅 화면까지 전체 흐름을 봅니다. 깊이 들어가기보다 각 기술이 어떤 역할을 맡고 어떻게 연결되는지에 집중합니다. 더 깊은 내용은 같은 저장소의 advanced 트랙에 있습니다.

### 2. 강의 전에 다섯 가지를 끝내 둔다

- 핵심 메시지: 설치와 키 발급은 강의 중에 하지 않는다. 사전 준비 가이드대로 미리 끝낸다
- 예상 시간: 0.5분
- 시각 자료: 체크리스트 표 (`table`)
- 본문 요약: Gemini API 키(Google AI Studio) | 저장소 최상위 .env의 GOOGLE_API_KEY에 값이 있다; Python 3.12(3.11~3.13) | python --version; Node.js 22 LTS 이상(최소 20.9) | node --version; Goose Desktop 설치와 연결 | 키를 연결하고 모델을 고른다 (화면은 부록); 패키지 설치 | pip install -r requirements.txt, npm --prefix labs/07-copilotkit-frontend install

스크립트:

> 60분 안에 설치와 키 발급까지 하기는 어렵습니다. 자세한 절차는 docs/prep-guide.md에 있습니다. 키 발급과 Goose 연결 화면은 덱 끝 부록(사전 준비 화면 6장)에 실제 화면으로 넣어 두었습니다. 가상환경은 python -m venv .venv로 만들고, 가상환경 활성화 뒤 pip install을 합니다. npm install은 처음에 몇 분 걸리므로 꼭 미리 해 두세요. 키가 아직 없는 분도 모의 모델로 흐름을 따라올 수 있습니다. 한국에서 무료 등급을 쓸 수 있는지는 확인하지 못했으니, 키를 받은 뒤 실습 L1을 미리 한 번 실행해 보라고 안내합니다.

### 3. 60분 동안 다섯 단계를 지난다

- 핵심 메시지: 모델 연결 → 에이전트 → 화면 → 보안 순서로 하나의 에이전트를 키운다
- 예상 시간: 0.5분
- 시각 자료: 목차 (`agenda`)
- 본문 요약: SESSION 1. AI 에이전트 플랫폼의 이해(5분) / SESSION 2. Gemini API 연결 및 Goose 활용(10분) / SESSION 3. AI 에이전트 개발(15분) / SESSION 4. AG-UI를 활용한 채팅 화면 구현(20분) / SESSION 5. 보안 및 해커톤 프로젝트 적용(10분)

스크립트:

> 오늘 흐름입니다. 세션 2에서 Gemini를 연결하고, 세션 3에서 ADK로 에이전트를 만들고, 세션 4에서 브라우저 화면에 붙입니다. 마지막에 보안과 해커톤 적용을 정리합니다. 실습은 세 번(L1, L2, L3)이고 모두 저장소 최상위 폴더에서 터미널 명령으로 실행합니다.

### 4. SESSION 1. AI 에이전트 플랫폼의 이해

- 핵심 메시지: AI 모델을 직접 개발하지 않아도 API를 활용하면 나만의 AI 에이전트 서비스를 만들 수 있다
- 예상 시간: 0.5분
- 시각 자료: 어두운 타일 섹션 표지 (`section`)
- 본문 요약: AI 모델을 직접 개발하지 않아도 API를 활용하면 나만의 AI 에이전트 서비스를 만들 수 있다

스크립트:

> 첫 세션은 5분입니다. LLM과 에이전트가 무엇이 다른지, 오늘 만들 것의 전체 그림을 봅니다.

### 5. LLM은 답하고, 에이전트는 도구로 일한다

- 핵심 메시지: 에이전트와 챗봇의 차이는 도구 실행과 반복 루프다
- 예상 시간: 1.5분
- 시각 자료: 좌우 비교 (`two_column`)
- 본문 요약: LLM 단독 호출: 입력 → 출력, 한 번에 끝난다; 파일을 읽거나 저장하지 못한다; 예: 문서를 붙여 넣고 요약을 받는다 ↔ AI 에이전트: 목표 → 계획 → 도구 실행 → 결과 반영; 필요하면 도구를 여러 번 부른다; 예: 문서를 읽고 분석해 보고서 파일로 저장한다

스크립트:

> 흔한 오해가 '에이전트는 똑똑한 챗봇'이라는 것입니다. LLM은 받은 글에 답을 만드는 모델 자체입니다. 에이전트는 목표를 받으면 모델의 판단으로 도구를 골라 실행하고, 그 결과를 보고 다시 판단합니다. 오늘 에이전트는 문서를 읽는 도구, 분석하는 도구, 보고서를 저장하는 도구 세 개를 씁니다.

### 6. 오늘 만들 에이전트는 네 층으로 연결된다

- 핵심 메시지: 모델·에이전트·도구·프론트엔드 네 층이 오늘의 전체 구조다
- 예상 시간: 1.5분
- 시각 자료: 전체 아키텍처 구성도 (`graph`)
- 본문 요약: 사용자 브라우저, Frontend CopilotKit 화면 :3000, Backend AG-UI 엔드포인트 :8000/ag-ui, ADK 에이전트, Gemini API, Tool 도구 3개, data/ · outputs/. 모델 gemini-3.5-flash-lite · 에이전트 doc_report_agent · 키는 Backend에만

스크립트:

> 이 그림을 오늘 계속 씁니다. 오른쪽 끝의 Gemini는 빌려 쓰는 모델입니다. 가운데 ADK 에이전트가 판단하고 도구를 부릅니다. 도구는 data/ 폴더의 문서를 읽고 outputs/에 보고서를 씁니다. 왼쪽의 브라우저 화면은 AG-UI라는 규격으로 Backend와 이벤트를 주고받습니다. API 키는 Backend에만 있고 브라우저에는 없습니다. Goose는 이 그림 밖에서 개발을 돕는 도구라는 점도 기억해 두세요.

## SESSION 2. Gemini API 연결 및 Goose 활용

### 7. SESSION 2. Gemini API 연결 및 Goose 활용

- 핵심 메시지: 키 하나와 모델 ID 하나로 어떤 도구에서든 같은 Gemini를 쓴다
- 예상 시간: 0.5분
- 시각 자료: 어두운 타일 섹션 표지 (`section`)
- 본문 요약: 키 하나와 모델 ID 하나로 어떤 도구에서든 같은 Gemini를 쓴다

스크립트:

> 세션 2는 10분입니다. 키를 코드에서 쓰는 방법과 Goose에 연결하는 방법을 봅니다.

### 8. 키 하나, 모델 ID 하나로 Gemini를 부른다

- 핵심 메시지: API 키는 .env의 GOOGLE_API_KEY 한 곳에만 둔다
- 예상 시간: 2분
- 시각 자료: 키 → .env → 모델 ID → 호출 흐름도 (`flow`)
- 본문 요약: 키 발급 → .env 등록 → 모델 ID → 호출. 키는 코드에 붙여 넣지 않는다 · 모델은 .env의 DOC_AGENT_MODEL만 고친다

스크립트:

> Google AI Studio에 로그인해 API 키를 발급합니다(실제 화면은 부록). Python 코드는 google-genai SDK로 Gemini를 부릅니다. 이 키를 저장소 최상위 .env의 GOOGLE_API_KEY에 넣습니다. SDK는 GEMINI_API_KEY와 GOOGLE_API_KEY를 모두 읽고, 둘 다 있으면 GOOGLE_API_KEY를 씁니다. 그래서 오늘은 GOOGLE_API_KEY 하나로 통일합니다. 모델 ID gemini-3.5-flash-lite는 공식 모델 페이지에서 Stable로 확인했고, 무료 등급에서 쓸 수 있습니다. 무료 등급의 분당·일일 한도 수치는 문서에 표로 나와 있지 않아 AI Studio에서 각자 확인합니다. (출처: aistudio.google.com/docs/api-key, aistudio.google.com/docs/models/gemini-3.5-flash-lite, aistudio.google.com/docs/rate-limits)

### 9. 실습 L1: Gemini API 연결 확인

- 핵심 메시지: 키와 모델 ID가 맞으면 코드 한 줄로 Gemini 응답을 받는다
- 예상 시간: 4분
- 시각 자료: 명령 상자와 기대 결과 상자 (`handson`)
- 본문 요약: 목표: 발급한 API 키로 Gemini에 문서 요약을 요청해 응답을 받는다<br>단계: 가상환경을 활성화한다 → .env에 GOOGLE_API_KEY가 있는지 본다 → hello_gemini.py를 실행해 3줄 요약을 본다 → 키가 없으면 --mock을 붙여 흐름만 본다 → 자동 확인(check.py)에서 CHECK OK를 본다<br>명령: `python labs/01-gemini-api/hello_gemini.py`<br>`python labs/01-gemini-api/check.py`<br>기대 결과: '모델 ID: gemini-3.5-flash-lite (Interactions API)', '문서: data/samples/project_status_report.md', '요약:' 아래 3줄 요약이 출력된다. 키가 없으면 python labs/01-gemini-api/hello_gemini.py --mock 으로 '모델 ID: gemini-3.5-flash-lite (모의 응답, API 호출 없음)'과 문서의 첫 글머리 3줄을 확인한다. check.py 마지막 줄은 CHECK OK

스크립트:

> 4분 실습입니다. 모든 명령은 저장소 최상위 폴더에서, 가상환경 활성화 뒤 실행합니다. hello_gemini.py는 Interactions API로 샘플 보고서를 3줄로 요약합니다. 'GOOGLE_API_KEY가 없습니다'가 나오면 .env가 없거나 새 터미널을 열지 않은 경우입니다. 429는 무료 등급 한도, 404는 모델 ID 오타입니다. 키가 없는 분은 --mock을 붙이면 API 호출 없이 같은 출력 형식을 볼 수 있습니다.

### 10. Goose는 같은 키로 코드를 대신 만든다

- 핵심 메시지: Goose는 이미 만들어진 에이전트 앱이고, 내 개발을 돕는 데 쓴다
- 예상 시간: 3.5분
- 시각 자료: 시연 3단계 카드 (`cards`)
- 본문 요약: 제공업체 연결 — '제공업체에 연결' → Google Gemini (API Key) → 키 입력 → 계속 / 모델 선택 — 키를 연결한 뒤 모델로 gemini-3.5-flash-lite를 선택한다 / 코드 만들기 — goose_prompts.md의 프롬프트로 doc_stats.py를 만들고 실행하게 한다

스크립트:

> 강사 시연입니다(3.5분). Goose Desktop은 AAIF의 오픈소스 데스크톱 AI 에이전트입니다. 카드의 순서와 이름은 사용자가 제공한 실제 화면(2026-11-15 캡처) 기준이고, 그 화면은 덱 끝 부록에 있습니다. Goose 화면의 '제공업체'는 이 강의에서 말하는 '프로바이더'와 같은 말입니다. 처음 실행하면 '제공업체에 연결' → 'Google Gemini (API Key)' → 'Google API Key' 칸에 키 입력 → '계속' 순서로 연결하고, 키를 연결한 뒤 모델로 gemini-3.5-flash-lite를 선택합니다. [공식 문서로만 확인] 이미 다른 설정으로 쓰고 있었다면 왼쪽 사이드바의 '설정'에서 프로바이더를 바꾸고, 모델 목록에 이 ID가 없으면 직접 입력할 수 있습니다(goose-docs.ai providers 페이지, 화면 이름은 영어 기준). 저장소 최상위 폴더를 작업 폴더로 두면 Developer 확장이 파일 편집과 터미널 명령 실행을 맡습니다. Goose가 명령을 실행하기 전에 무엇을 하려는지 읽고 확인하세요. Goose가 doc_stats.py를 만드는 과정은 캡처가 없어 라이브로 보여 줍니다.

## SESSION 3. AI 에이전트 개발

### 11. SESSION 3. AI 에이전트 개발

- 핵심 메시지: ADK 에이전트는 Model + Instruction + Tool 세 줄로 시작한다
- 예상 시간: 0.5분
- 시각 자료: 어두운 타일 섹션 표지 (`section`)
- 본문 요약: ADK 에이전트는 Model + Instruction + Tool 세 줄로 시작한다

스크립트:

> 세션 3은 15분입니다. ADK로 에이전트를 정의하는 코드를 읽고 실제로 실행합니다.

### 12. 에이전트 = Model + Instruction + Tool

- 핵심 메시지: ADK 에이전트는 Model·Instruction·Tool을 root_agent 하나에 담는다
- 예상 시간: 3분
- 시각 자료: 네 구성 요소 카드 (`cards`)
- 본문 요약: Model — 판단하는 두뇌. gemini-3.5-flash-lite를 API로 빌려 쓴다 / Instruction — 역할과 답변 규칙을 적은 지시문 / Tool — docstring(설명)과 타입이 있는 Python 함수 (Function Tool) / MCP — 도구를 표준 플러그처럼 붙이는 규격 (실습은 advanced 트랙)

스크립트:

> Google ADK는 에이전트를 코드로 정의하고 실행하는 프레임워크입니다. Goose는 완성된 앱이고, ADK는 내 에이전트를 만드는 도구라는 점이 다릅니다. 에이전트에는 세 가지가 필요합니다. 판단할 모델, 역할을 적은 Instruction, 호출할 Tool입니다. Python 함수에 타입 힌트와 docstring을 쓰면 그것이 모델에게 주는 도구 설명이 됩니다. MCP는 도구를 표준 방식으로 붙이는 규격인데 오늘은 개념만 소개합니다. 참고로 도구 함수 하나쯤은 Goose에게 만들어 달라고 할 수도 있습니다.

### 13. root_agent 하나가 에이전트 전체다

- 핵심 메시지: Model·Instruction·Tool 세 인자로 에이전트를 만든다
- 예상 시간: 3.5분
- 시각 자료: agent.py 코드 (`code`)
- 본문 요약: `labs/04-function-tools/doc_report_agent/agent.py` 21–27행. model: 모델 ID (.env의 DOC_AGENT_MODEL) instruction: 위쪽 파일 14~19행의 지시문 tools: 함수 세 개를 그대로 넘긴다 ADK는 root_agent라는 변수를 찾는다

스크립트:

> labs/04-function-tools/doc_report_agent/agent.py의 21~27행입니다. 강조한 세 줄은 파일 23행(model), 25행(instruction), 26행(tools)입니다. model에는 모델 ID가 들어갑니다. mock이면 키 없이 도는 모의 모델이 들어갑니다. instruction은 바로 위에 있는 지시문으로, 문서를 읽고 분석해 요약·핵심 항목·문제점·보고서 순서로 답하고 저장하라고 적혀 있습니다. tools에는 tools.py의 함수 세 개를 넘깁니다. ADK는 root_agent라는 이름의 변수를 찾으므로 이름을 바꾸지 않습니다.

### 14. 실습 L2: ADK 문서 분석 에이전트 실행

- 핵심 메시지: 에이전트가 도구 세 개를 순서대로 불러 보고서를 저장한다
- 예상 시간: 8분
- 시각 자료: 명령 상자와 기대 결과 상자 (`handson`)
- 본문 요약: 목표: ADK 개발 UI에서 문서 분석 에이전트에 샘플 문서를 분석·요약·보고서 작성하게 하고 도구 호출을 확인한다<br>단계: 개발 UI(adk web)를 8080 포트로 띄운다 → 브라우저에서 doc_report_agent를 고른다 → '샘플 보고서를 분석해 줘'를 입력한다 → 이벤트 패널에서 도구 호출 순서를 본다 → 자동 확인(check.py)에서 CHECK OK를 본다<br>명령: `adk web --port 8080 labs/04-function-tools`<br>`python labs/04-function-tools/check.py`<br>기대 결과: http://localhost:8080 에서 doc_report_agent를 고르고 '샘플 보고서를 분석해 줘'라고 입력하면 read_document -> analyze_document -> save_report 도구 호출과 요약·핵심 항목·문제점이 담긴 답, '보고서를 outputs/<날짜-시각>_스마트_배송_앱_프로젝트_주간_현황_보고.md에 저장했습니다.'가 보인다. check.py는 '도구 호출 순서: read_document -> analyze_document -> save_report'와 CHECK OK를 출력한다

스크립트:

> 8분 실습입니다. adk web은 ADK의 개발 UI로, 운영용이 아니라 개발 확인용입니다. 포트는 Backend와 겹치지 않게 항상 8080을 씁니다. 처음 실행하면 'Enable telemetry? [Y/n]'을 물을 수 있습니다. adk를 못 찾으면 가상환경이 활성화되지 않은 것이고, 8080이 사용 중이면 다른 프로그램을 끕니다. 이벤트 패널에서 read_document, analyze_document, save_report가 차례로 호출되는 것을 확인하세요.

## SESSION 4. AG-UI를 활용한 채팅 화면 구현

### 15. SESSION 4. AG-UI를 활용한 채팅 화면 구현

- 핵심 메시지: 에이전트는 Backend에서 동작하지만 AG-UI를 통해 친숙한 서비스 화면으로 제공할 수 있다
- 예상 시간: 0.5분
- 시각 자료: 어두운 타일 섹션 표지 (`section`)
- 본문 요약: 에이전트는 Backend에서 동작하지만 AG-UI를 통해 친숙한 서비스 화면으로 제공할 수 있다

스크립트:

> 세션 4는 20분으로 가장 깁니다. 같은 에이전트를 브라우저 채팅 화면에 붙입니다.

### 16. AG-UI 이벤트가 화면을 만든다

- 핵심 메시지: Backend가 보내는 AG-UI 이벤트를 CopilotKit이 채팅 화면으로 그린다
- 예상 시간: 4분
- 시각 자료: 요청·이벤트 흐름도 (`flow`)
- 본문 요약: 브라우저 → CopilotKit 런타임 → AG-UI 엔드포인트 → ADK 에이전트 → Gemini API. 이벤트: RUN_STARTED → TOOL_CALL_START → TEXT_MESSAGE_CONTENT → RUN_FINISHED

스크립트:

> 요청은 왼쪽에서 오른쪽으로, 이벤트는 오른쪽에서 왼쪽으로 흐릅니다. 에이전트는 Python Backend(8000번 포트)에서 돌고, 화면은 Next.js Frontend(3000번 포트)입니다. AG-UI는 Backend와 화면 사이의 이벤트 규격입니다. 실행 시작, 글자 조각, 도구 호출, 실행 종료 같은 이벤트가 정해져 있고, 전송되는 type 값은 RUN_STARTED처럼 대문자 스네이크 케이스입니다. 흔한 오해가 'CopilotKit = AG-UI'입니다. AG-UI는 프로토콜이고, CopilotKit은 그 프로토콜을 쓰는 프론트엔드 프레임워크입니다. AG-UI는 CopilotKit에서 시작된 오픈 프로토콜입니다. ADK와 AG-UI 연동은 AG-UI 문서와 ADK 문서 양쪽에서 공식 지원으로 확인했습니다.

### 17. 실습 L3: 브라우저 채팅 화면 연결

- 핵심 메시지: 터미널 두 개로 Backend와 Frontend를 띄우면 브라우저에서 에이전트와 대화한다
- 예상 시간: 12분
- 시각 자료: 명령 상자와 기대 결과 상자 (`handson`)
- 본문 요약: 목표: AG-UI 백엔드와 CopilotKit 프론트엔드를 띄워 브라우저에서 문서 분석 에이전트와 대화한다<br>단계: 터미널 1에서 Backend(server.py)를 띄운다 → 터미널 2에서 Frontend를 띄운다(install은 사전 준비에서 완료) → http://localhost:3000 을 연다 → 문서 내용을 붙여 넣거나 '샘플 보고서를 분석해 줘'를 입력한다<br>명령: `python labs/06-agui-backend/server.py`<br>`npm --prefix labs/07-copilotkit-frontend install`<br>`npm --prefix labs/07-copilotkit-frontend run dev`<br>기대 결과: http://localhost:3000 채팅 창에 문서 내용(예: data/samples/meeting_notes.md)을 붙여 넣으면 답이 조각 단위로 흘러나오고, 'analyze_document 완료 핵심 항목 5개, 문제점 3개', 'save_report 완료 저장: outputs/...md' 도구 상태 카드와 오른쪽 '보고서 결과' 패널(제목·핵심 항목·문제점·저장 경로)이 표시된다. check.py는 정적 검사와 Backend 왕복 후 CHECK OK를 출력한다

스크립트:

> 12분 실습입니다. 터미널이 두 개 필요합니다. 첫 터미널에서 Backend를 띄우고, 두 번째 터미널에서 Frontend를 띄웁니다. npm install은 사전 준비에서 했다면 건너뜁니다. Backend를 띄우지 않고 화면을 열면 연결 오류가 납니다. 시간이 밀리면 이 실습은 강사 시연으로 바꿉니다. 확인이 끝나면 python labs/07-copilotkit-frontend/check.py로 CHECK OK를 볼 수 있습니다.

### 18. 최종 시연: 채팅과 보고서 패널이 함께 움직인다

- 핵심 메시지: 브라우저에서 스트리밍 답, 도구 실행 상태, 보고서 결과를 한 화면에 본다
- 예상 시간: 3.5분
- 시각 자료: 최종 화면 구성도(좌: 채팅, 우: 보고서) (`two_column`)
- 본문 요약: 왼쪽 — 채팅: 입력: 샘플 보고서를 분석해 줘; 답이 조각 단위로 흘러나온다; 도구 상태 카드: read_document → analyze_document → save_report ↔ 오른쪽 — 보고서 결과 패널: 제목; 핵심 항목과 문제점; 저장 경로: outputs/…md

스크립트:

> 최종 시연입니다. 시나리오는 docs/basic/demo-scenario.md를 따릅니다. 왼쪽 채팅에 '샘플 보고서를 분석해 줘'를 보내면 답이 조각으로 흘러나오고, 그 사이에 도구 상태 카드가 생깁니다. 예를 들어 'analyze_document 완료 핵심 항목 5개, 문제점 6개', 'save_report 완료 저장: outputs/...md'가 보입니다. 오른쪽 보고서 결과 패널에는 제목, 핵심 항목, 문제점, 저장 경로가 나타납니다. 이 구성은 실제 코드(page.tsx, ToolStatus.tsx, ReportPanel.tsx)에서 그린 화면 구성도입니다. 실제 화면은 라이브로 보여 줍니다.

## SESSION 5. 보안 및 해커톤 프로젝트 적용

### 19. SESSION 5. 보안 및 해커톤 프로젝트 적용

- 핵심 메시지: 키는 Backend에, 권한은 최소로, 문서는 데이터로
- 예상 시간: 0.5분
- 시각 자료: 어두운 타일 섹션 표지 (`section`)
- 본문 요약: 키는 Backend에, 권한은 최소로, 문서는 데이터로

스크립트:

> 마지막 세션 10분입니다. 서비스로 내놓기 전에 지킬 것과 내 아이디어에 적용하는 방법을 봅니다.

### 20. 보안 체크리스트 핵심 여섯 가지

- 핵심 메시지: 키는 Backend에, 권한은 최소로, 문서는 데이터로
- 예상 시간: 4분
- 시각 자료: 체크리스트 표 (`table`)
- 본문 요약: SEC-01 | API 키를 코드·저장소에 두지 않고 .env에만 둔다 | .env를 .gitignore에 등록; SEC-03 | 브라우저(Frontend)에 키를 두지 않고 Backend를 거쳐 호출한다 | CopilotKit 런타임 → /ag-ui; SEC-05 | 에이전트가 읽고 쓰는 폴더를 허용 목록(data/, outputs/)으로 제한한다 | read_document 경로 검사; SEC-06 | MCP 도구는 필요한 것만 열고, 위험한 도구는 실행 전 사용자 승인을 받는다 | McpToolset의 tool_filter; SEC-07 | 문서·웹 내용은 지시가 아니라 데이터로 다루고 프롬프트 인젝션을 찾아낸다 | advanced 트랙 실습 L11; SEC-09 | 무료 등급 입력은 제품 개선에 쓰일 수 있으므로 민감·개인 정보를 넣지 않는다 | 가상 샘플 문서만 사용

스크립트:

> 번호(SEC-01~12)는 docs/security-checklist.md에 있는 보안·거버넌스 체크리스트의 항목 번호이고, 오늘은 그중 여섯 가지만 봅니다. SEC-06은 Goose의 권한 모드에도 해당합니다(Goose 권한 모드 화면은 확인하지 못함). 가장 흔한 실수는 '.gitignore에 .env를 넣었으니 안전하다'는 생각입니다. 이미 커밋한 키는 이력에 남으므로 새 키를 발급해야 합니다. 무료 등급은 입력이 제품 개선에 쓰일 수 있다고 가격 페이지에 적혀 있습니다. 실제 고객 데이터나 개인 정보는 넣지 마세요. SEC-07 인젝션 대응은 advanced 트랙 L11에서 직접 가드레일로 구현합니다.

### 21. 내 아이디어는 역할·도구·화면 세 칸으로 옮긴다

- 핵심 메시지: 문서 분석 에이전트의 뼈대는 두고 Instruction과 Tool만 바꾸면 내 서비스가 된다
- 예상 시간: 5.5분
- 시각 자료: 3단계 카드 + 다음 단계 (`cards`)
- 본문 요약: 역할 — Instruction: 누구를 돕고, 무엇을 하고, 어떻게 답하는가 / 도구 — Tool: 에이전트가 부를 함수 1~3개 (입력과 출력) / 화면 — AG-UI: 채팅 옆에 보여 줄 도구 카드와 결과 패널 / 다음 단계 — advanced 트랙, labs/09 템플릿, 해커톤 확장 가이드

스크립트:

> 마무리입니다. 해커톤 아이디어를 세 칸으로 옮겨 보세요. 역할은 Instruction, 도구는 Tool 함수, 화면은 오늘 본 CopilotKit 화면입니다. labs/09-final-project에는 Instruction과 Tool만 바꾸면 되는 템플릿이 있고, 같은 화면에 그대로 연결됩니다. 더 깊이 보고 싶으면 같은 저장소의 advanced 트랙과 해커톤 서비스 확장 가이드(docs/hackathon-extension-guide.md)를 참고하세요. 질문 받겠습니다.

[출처] 오늘 자료의 기술 사실은 2026-11-15에 공식 문서로 확인했다. 전체 출처와 확인하지 못한 항목은 docs/tech-verification.md에 있다. Gemini API: aistudio.google.com/docs/pricing, /docs/api-key, /docs/interactions-overview · Goose: goose-docs.ai/docs/getting-started/providers · Google ADK: adk.dev/get-started/python · MCP: modelcontextprotocol.io/specification/latest · AG-UI: docs.ag-ui.com/introduction, docs.ag-ui.com/concepts/events · CopilotKit: docs.copilotkit.ai/adk, adk.dev/integrations/copilotkit

## 시작·마무리

### 22. 부록: 사전 준비 화면

- 핵심 메시지: 사전 준비는 이 화면 6장을 따라 하면 된다
- 예상 시간: 0분
- 시각 자료: 부록 표지 (`section`)
- 본문 요약: API 키 발급과 Goose 연결을 실제 화면으로 따라 한다 (발표 시간 외)

스크립트:

> 부록입니다. 60분 발표 시간에는 넣지 않았습니다. 사전 준비를 하는 수강생이나 질문이 나왔을 때 보여 줍니다. 화면은 사용자가 제공한 실제 화면(2026-11-15 캡처)이고, 키와 개인 정보는 회색 상자로 가렸습니다.

### 23. 'API 키 만들기'를 누른다

- 핵심 메시지: Google AI Studio의 API 키 화면에서 새 키를 만든다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 aistudio-2-api-keys.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] aistudio.google.com에 Google 계정으로 로그인하고 왼쪽 아래 열쇠 아이콘을 누르면 이 API 키 화면이 나옵니다. 오른쪽 위 'API 키 만들기'를 누릅니다.

### 24. 키 이름과 프로젝트를 정하고 '키 만들기'를 누른다

- 핵심 메시지: 키 이름과 프로젝트를 정하면 키가 만들어진다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 aistudio-3-create-key.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] '새 키 만들기' 창입니다. 키 이름은 알아보기 쉬운 이름이면 됩니다(화면 예: Gemini API Key). 프로젝트를 고르고 '키 만들기'를 누릅니다. 화면의 프로젝트 이름은 예시이고 각자 다릅니다.

### 25. '키 복사'로 복사해 .env에만 붙여 넣는다

- 핵심 메시지: 복사한 키는 .env의 GOOGLE_API_KEY에만 넣는다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 aistudio-4-key-detail.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] '키 복사'를 누르고 저장소 최상위 .env 파일의 GOOGLE_API_KEY= 뒤에 붙여 넣습니다. 따옴표는 붙이지 않습니다. 화면의 키·프로젝트 정보는 가렸습니다. 복사한 키는 채팅, 코드, 스크린샷에 붙이지 않습니다. Goose에도 같은 키를 넣으므로 잠시 복사해 둡니다.

### 26. Goose 첫 화면에서 '제공업체에 연결'을 누른다

- 핵심 메시지: Goose는 처음 실행할 때 AI 모델 제공업체(프로바이더)를 연결한다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 goose-1-welcome.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] Goose Desktop을 처음 실행한 화면입니다. '로컬 모델 사용'과 '제공업체에 연결' 중 '제공업체에 연결'을 누릅니다. Goose 화면의 '제공업체'는 이 강의의 '프로바이더'와 같은 말입니다.

### 27. Google Gemini (API Key)를 고르고 키를 넣는다

- 핵심 메시지: 제공업체는 Google Gemini (API Key), 키는 Google API Key 칸에 넣는다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 goose-2-provider.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] 목록에서 'Google Gemini (API Key)'를 고르고 'Google API Key' 칸에 복사한 키를 붙여 넣은 뒤 '계속'을 누릅니다. 화면에 '키는 키체인에 안전하게 저장됩니다'라고 나옵니다. 키를 연결한 뒤 모델로 gemini-3.5-flash-lite를 선택합니다(모델을 고르는 화면은 캡처가 없어 넣지 않았습니다).

### 28. 한국어로 말을 걸어 답이 오면 연결 끝

- 핵심 메시지: 키를 연결한 뒤 gemini-3.5-flash-lite를 선택하면 입력창 아래에 모델 이름이 보인다
- 예상 시간: 0분
- 시각 자료: 화면 캡처 goose-4-chat.png + 누를 곳 강조 상자 (`image`)
- 본문 요약: 

스크립트:

> [부록 · 발표 시간 외] 키를 연결한 뒤 모델로 gemini-3.5-flash-lite를 선택하면 채팅 화면이 나옵니다. 한국어로 '안녕 :) 자기소개 부탁해.'처럼 말을 걸어 답이 오면 연결이 끝난 것입니다. 입력창 아래의 모델 이름이 gemini-3.5-flash-lite인지 확인합니다. 작업 폴더 경로는 가렸습니다.
