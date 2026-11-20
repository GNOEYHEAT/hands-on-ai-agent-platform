# 전체 교육과정 기획서

AI 에이전트 플랫폼 개발 Hands-on. 하나의 공통 프로젝트(문서 분석 및 보고서 작성 AI 에이전트, 코드 이름 `doc_report_agent`)를 두 가지 길이로 가르친다.

## 대상

AI 기반 서비스·창업 아이디어를 기획하는 해커톤 참가자(기획자와 개발자 혼합). 터미널 명령을 실행하고 Python 기초 문법을 읽을 수 있으면 된다. JavaScript/TypeScript는 몰라도 되며 프론트엔드는 완성본을 제공한다.

## 두 트랙

| | basic | advanced |
| --- | --- | --- |
| 수준 | 초급 | 초급~중급 |
| 시간 | 60분 | 300분(모듈 275분 + 휴식·질의응답 25분, 점심 별도) |
| 구성 | SESSION 1–5 (M1–M5) | PART 1–5 (M6–M10) |
| 실습 | L1–L3 (24분) + 강사 시연 | L4–L12 (170분) |
| 방식 | 개념 설명 30%, 실습 및 시연 70%(실습 40% + 강사 시연 30%) | 개념 설명 30%, 실습 70%(실습 약 62% + 따라 하기 시연) |
| 목표 | 전체 흐름을 보고 가능성을 경험한다 | 직접 구현하고 프로토타입을 만든다 |

basic은 별도 코드가 없다. basic 실습은 advanced 실습 폴더(`labs/01-gemini-api`, `labs/04-function-tools`, `labs/06-agui-backend`와 `labs/07-copilotkit-frontend`)를 그대로 실행한다.

## 학습 목표

1. Google AI Studio에서 Gemini API 키를 발급해 환경 변수로 등록하고 Python 코드에서 Gemini 응답을 받는다
2. Goose Desktop에 Gemini 프로바이더와 모델을 설정하고 로컬 파일을 읽어 코드를 만들게 한다
3. Google ADK로 Model·Instruction·Tool을 갖춘 문서 분석 에이전트를 만들고 실행한다
4. Function Tool과 MCP 서버로 에이전트에 외부 기능을 연결한다
5. AG-UI와 CopilotKit으로 에이전트와 대화하는 웹 채팅 화면을 띄우고 도구 실행 상태를 표시한다
6. API 키 관리·접근 제어·프롬프트 인젝션 대응을 보안·거버넌스 체크리스트로 점검한다
7. 자신의 서비스 아이디어를 에이전트 역할·도구·화면으로 설계해 프로토타입을 만든다

basic은 목표 4(Function Tool과 MCP 서버)를 개념 소개 수준으로만 다룬다.

## 공통 프로젝트가 발전하는 순서

1. Gemini API 연결(`labs/01-gemini-api`)
2. Goose로 개발 환경 활용(`labs/02-goose-devenv`)
3. Google ADK로 에이전트 구현(`labs/03-adk-agent`)
4. Function Tool로 문서 분석 확장(`labs/04-function-tools`)
5. MCP 연동(`labs/05-mcp-tools`)
6. AG-UI와 CopilotKit 웹 인터페이스(`labs/06-agui-backend`, `labs/07-copilotkit-frontend`)
7. 보안 가드레일(`labs/08-security-governance`)
8. 내 서비스 프로토타입(`labs/09-final-project`)

## 운영 방식

- 실습 환경: Windows 또는 macOS, Python 3.12(3.11~3.13), Node.js 22 LTS 이상, Git, Goose Desktop. 사전 준비는 [사전 준비 가이드](prep-guide.md)로 강의 전에 끝낸다.
- 외부 계정: Google 계정 하나(AI Studio 키). 유료 결제와 GPU는 필요 없다.
- 모델: `gemini-3.5-flash-lite`(`.env`의 `DOC_AGENT_MODEL`로 교체). 무료 등급 입력은 제품 개선에 쓰일 수 있으므로 샘플 문서(`data/samples/`, 모두 가상 데이터)만 쓴다.
- 키가 없어도 모든 흐름을 볼 수 있도록 모의 모델(`DOC_AGENT_MODEL=mock`)을 둔다. 자동 검증(`check.py`)은 항상 모의 모델로 키 없이 돈다.
- 포트: AG-UI Backend 8000, ADK 개발 UI(`adk web`) 8080, Next.js 3000.

## 운영 시 가정

- advanced는 사용자가 정한 1일 5시간(09:00–12:00, 13:00–15:00, 300분)에 맞췄다. 내용은 줄이지 않고 시간 배분만 바꿨다. 다 하지 못한 실습 확장과 PART 5 확장판(90분)은 강의 뒤에 이어서 한다. 2일 과정으로 늘리면 PART 5를 2일차 전체(해커톤 개발 시간)로 확장한다.
- basic은 SESSION별 시간(5/10/15/20/10분)이 정해져 있어 여유 시간이 없다. 시간이 밀리면 SESSION 4의 실습을 강사 시연으로 바꾼다.
- PART 5 프로토타입은 1~3인 팀을 가정했다. 강의 중에는 희망하는 2팀이 2분씩 발표하고, 확장판(강의 뒤)에서는 팀당 3분 발표한다.

## 산출물

| 산출물 | 위치 |
| --- | --- |
| 학습 가이드(트랙별 Hands-on) | [README.md](../README.md) |
| 슬라이드 | `slides/hands-on-ai-agent-platform-basic.pptx`, `slides/hands-on-ai-agent-platform-advanced.pptx` |
| 강사용 스크립트 | [basic](instructor/basic-script.md), [advanced](instructor/advanced-script.md) |
| 시간 배분과 상세 목차 | [basic 구성표](basic/session-plan.md), [advanced 커리큘럼](advanced/curriculum.md) |
| 아키텍처, 기술 검증, 보안 체크리스트 | [architecture.md](architecture.md), [tech-verification.md](tech-verification.md), [security-checklist.md](security-checklist.md) |
| 최종 프로젝트, 확장 가이드 | [final-project-guide.md](advanced/final-project-guide.md), [hackathon-extension-guide.md](hackathon-extension-guide.md) |
| 실습 코드 | `labs/`, `data/samples/` |
