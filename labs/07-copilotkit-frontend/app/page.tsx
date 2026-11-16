"use client";

import { CopilotChat } from "@copilotkit/react-core/v2";
import { AGENT_ID } from "./agent";
import { ReportPanel } from "./components/ReportPanel";
import { useToolStatusCards } from "./components/ToolStatus";

export default function Home() {
  useToolStatusCards(); // 도구 실행 상태를 채팅 안에 카드로 그린다

  return (
    <main className="layout">
      <section className="chat">
        <h1>문서 분석 및 보고서 작성 AI 에이전트</h1>
        <CopilotChat
          agentId={AGENT_ID}
          labels={{ chatInputPlaceholder: "문서 내용을 붙여 넣거나 '샘플 보고서를 분석해 줘'라고 입력하세요" }}
        />
      </section>
      <ReportPanel />
    </main>
  );
}
