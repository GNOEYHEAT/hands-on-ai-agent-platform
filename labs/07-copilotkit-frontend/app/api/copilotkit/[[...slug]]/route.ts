// CopilotKit 런타임: 브라우저 요청을 Backend의 AG-UI 엔드포인트로 전달한다.
// API 키는 Backend(Python)에만 있다. 브라우저는 이 경로(/api/copilotkit)만 부른다(SEC-03).
import { HttpAgent } from "@ag-ui/client";
import {
  CopilotRuntime,
  InMemoryAgentRunner,
  createCopilotRuntimeHandler,
} from "@copilotkit/runtime/v2";

const AG_UI_URL = process.env.ADK_AG_UI_URL ?? "http://localhost:8000/ag-ui";

const runtime = new CopilotRuntime({
  // 이 이름(doc_report_agent)이 화면의 agentId와 같아야 한다.
  agents: { doc_report_agent: new HttpAgent({ url: AG_UI_URL }) },
  runner: new InMemoryAgentRunner(),
});

const handler = createCopilotRuntimeHandler({ runtime, basePath: "/api/copilotkit" });

export { handler as GET, handler as POST, handler as PATCH, handler as DELETE };
