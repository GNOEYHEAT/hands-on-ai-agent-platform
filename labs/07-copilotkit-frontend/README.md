# L3·L10 CopilotKit 채팅 화면

이 실습에서는 Next.js와 CopilotKit으로 만든 채팅 화면을 AG-UI Backend(L9)에 연결합니다. 화면에는 스트리밍 응답, 도구 실행 상태, 보고서 결과가 표시됩니다.

- L3은 basic 트랙의 실습 3, L10은 advanced 트랙의 실습 10입니다. 같은 코드를 씁니다.
- Next.js는 React로 웹 화면을 만드는 프레임워크입니다.
- CopilotKit은 AG-UI 이벤트를 받아 채팅 화면으로 그려 주는 프론트엔드 프레임워크입니다.
- Frontend는 사용자가 보는 웹 화면(3000번 포트), Backend는 에이전트가 실행되는 Python 서버(8000번 포트)입니다.

## 구조

```
labs/07-copilotkit-frontend/
├── app/
│   ├── api/copilotkit/[[...slug]]/route.ts   CopilotKit 런타임: HttpAgent로 Backend(/ag-ui)에 연결
│   ├── agent.ts                              AGENT_ID = "doc_report_agent"
│   ├── providers.tsx                         <CopilotKit runtimeUrl="/api/copilotkit">
│   ├── layout.tsx
│   ├── page.tsx                              <CopilotChat agentId=...> + 보고서 패널
│   ├── components/ToolStatus.tsx             useRenderTool로 도구 실행 상태 카드
│   ├── components/ReportPanel.tsx            useAgent로 대화 기록에서 분석·저장 결과를 꺼내 표시
│   └── globals.css
├── package.json, package-lock.json           버전 고정
└── check.py
```

요청은 브라우저(CopilotChat) → `/api/copilotkit`(CopilotKit 런타임) → `http://localhost:8000/ag-ui`(ag-ui-adk) → ADK 에이전트 → Gemini 순서로 갑니다. 이벤트는 반대 방향으로 돌아옵니다. CopilotKit 런타임은 Next.js 서버 안에서 브라우저의 요청을 Backend로 전달하는 부분입니다. API 키는 Backend에만 있습니다(SEC-03).

## 실행

이 실습에는 터미널이 2개 필요합니다. 두 터미널 모두 저장소 최상위 폴더에서 진행합니다.

1. 터미널 1에서 Backend를 띄우세요. 터미널 1은 가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널이어야 합니다. 이 터미널은 끄지 말고 그대로 두세요.

   ```
   python labs/06-agui-backend/server.py
   ```

2. 터미널 2를 새로 열고 Frontend에 필요한 패키지를 설치하세요. 처음 한 번만 하면 됩니다(이 강의를 만든 PC에서 약 5분, 패키지 1176개).

   ```
   npm --prefix labs/07-copilotkit-frontend install
   ```

3. 터미널 2에서 Frontend 개발 서버를 띄우세요. 이 터미널도 그대로 두세요.

   ```
   npm --prefix labs/07-copilotkit-frontend run dev
   ```

4. 브라우저 주소창에 http://localhost:3000 을 입력하세요.
5. 채팅 창에 다음 중 하나를 입력하세요.
   - `샘플 보고서를 분석해 줘`
   - 문서 내용 붙여 넣기(예: `data/samples/meeting_notes.md` 전체)

화면 왼쪽에 답이 흘러나오고, 그 사이에 `analyze_document 완료 핵심 항목 5개, 문제점 3개`, `save_report 완료 저장: outputs/...md` 같은 도구 상태 카드가 생깁니다. 오른쪽 "보고서 결과" 패널에는 제목, 핵심 항목, 문제점, 저장 경로가 나타납니다.

## Backend 주소 바꾸기

기본 주소는 `http://localhost:8000/ag-ui`입니다. Next.js는 저장소 최상위의 `.env`를 읽지 않습니다. 주소를 바꿔야 하면 이 폴더에 `.env.local` 파일을 만들고 `ADK_AG_UI_URL=http://localhost:8001/ag-ui`처럼 적으세요. 이 파일은 `.gitignore`에 들어 있어 저장소에 올라가지 않습니다. API 키는 이 파일에 넣지 마세요.

## 해 볼 것

`components/ToolStatus.tsx`에는 `analyze_document`, `save_report` 전용 카드와, 나머지 도구에 쓰는 `"*"` 카드가 있습니다. `read_document` 전용 카드를 추가해 읽은 파일 경로를 보여 주세요. 아래 코드를 `useToolStatusCards` 함수 안에 넣으면 됩니다.

```tsx
useRenderTool(
  {
    name: "read_document",
    agentId: AGENT_ID,
    parameters: z.object({ path: z.string() }),
    render: ({ status, parameters }) => (
      <StatusCard title="read_document" status={status} detail={`읽는 파일: data/${parameters.path ?? ""}`} />
    ),
  },
  [],
);
```

## 확인

저장소 최상위 폴더에서 다음 명령 중 하나를 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

```
python labs/07-copilotkit-frontend/check.py            # 정적 검사 + Backend 왕복(Node.js 불필요)
python labs/07-copilotkit-frontend/check.py --build    # + npm install, npm run build
python labs/07-copilotkit-frontend/check.py --e2e      # + next dev를 띄워 런타임 경유 왕복(npm install 후)
```

`--e2e`는 같은 폴더에서 Frontend 개발 서버를 하나 더 띄웁니다. Next.js는 한 폴더에서 개발 서버가 두 개 뜨는 것을 막으므로, 터미널 2의 Frontend가 켜져 있으면 `--e2e`가 실패합니다(`ConnectionResetError` 같은 오류로 끝납니다). `--e2e`를 실행하기 전에 터미널 2에서 Ctrl+C를 눌러 Frontend를 끄세요. 터미널 1의 Backend는 켜 둔 채로 실행해도 됩니다. 옵션 없는 기본 검사와 `--build`는 Frontend를 켜 둔 채로 실행해도 됩니다.

## 막히면

| 화면에 보이는 것 | 원인과 해결 |
| --- | --- |
| 채팅을 보내도 답이 없음 | 터미널 1의 Backend가 꺼져 있습니다. `python labs/06-agui-backend/server.py`로 다시 띄우세요 |
| 에이전트를 찾지 못했다는 오류(`Agent 'doc_report_agent' not found` 류) | `app/agent.ts`의 `AGENT_ID`와 `route.ts`의 `agents` 키가 다릅니다. 두 값을 같게 맞추세요 |
| `npm`이 Node 버전 오류를 냄 | Node.js 20.9 이상이 필요합니다(22 LTS 권장) |
| 3000 포트를 이미 쓰고 있다는 오류 | `npm --prefix labs/07-copilotkit-frontend run dev -- --port 3001`로 다른 포트를 쓰세요 |

CopilotKit 런타임은 기본으로 익명 사용 통계를 보냅니다. 끄려면 Frontend 서버를 켜기 전에 같은 터미널(터미널 2)에서 환경 변수 `COPILOTKIT_TELEMETRY_DISABLED`를 `true`로 정하세요(Next.js의 사용 통계는 `NEXT_TELEMETRY_DISABLED`를 `1`로). 환경 변수를 정하는 방법은 최상위 README의 [터미널에서 환경 변수를 잠깐 정하는 법](../../README.md#터미널에서-환경-변수를-잠깐-정하는-법)에 있습니다. 개발 서버 로그에 보이는 `[CopilotKit] Listing and clearing threads need a caller identity...` 경고는 스레드 목록 기능을 쓰지 않는 이 실습에서는 무시해도 됩니다.
