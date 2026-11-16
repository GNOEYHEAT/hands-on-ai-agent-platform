"use client";

import { useAgent } from "@copilotkit/react-core/v2";
import { AGENT_ID } from "../agent";

type Analysis = { title?: string; key_points?: string[]; issues?: string[] };
type AnyMessage = {
  role: string;
  content?: unknown;
  toolCallId?: string;
  toolCalls?: { id: string; function: { name: string } }[];
};

// 대화 기록에서 가장 최근 도구 결과(JSON 문자열)를 찾는다.
function latestResult(messages: AnyMessage[], toolName: string): Record<string, unknown> | null {
  const ids = messages.flatMap((m) => (m.toolCalls ?? []).filter((c) => c.function.name === toolName).map((c) => c.id));
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m.role === "tool" && m.toolCallId && ids.includes(m.toolCallId) && typeof m.content === "string") {
      try {
        return JSON.parse(m.content);
      } catch {
        return null;
      }
    }
  }
  return null;
}

export function ReportPanel() {
  const { agent } = useAgent({ agentId: AGENT_ID });
  const messages = agent.messages as unknown as AnyMessage[];
  const analysis = latestResult(messages, "analyze_document") as Analysis | null;
  const saved = latestResult(messages, "save_report") as { path?: string } | null;

  return (
    <aside className="report">
      <h2>보고서 결과</h2>
      {!analysis && <p className="muted">분석이 끝나면 여기에 제목, 핵심 항목, 문제점이 표시됩니다.</p>}
      {analysis && (
        <>
          <h3>{analysis.title}</h3>
          <h4>핵심 항목</h4>
          <ul>{analysis.key_points?.map((item) => <li key={item}>{item}</li>)}</ul>
          <h4>문제점</h4>
          <ul>{analysis.issues?.map((item) => <li key={item}>{item}</li>)}</ul>
        </>
      )}
      {saved?.path && <p className="saved">저장된 보고서: {saved.path}</p>}
    </aside>
  );
}
