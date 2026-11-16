"use client";

import { useRenderTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { AGENT_ID } from "../agent";

type Status = "inProgress" | "executing" | "complete";

function StatusCard({ title, status, detail }: { title: string; status: Status; detail?: string }) {
  const label = status === "complete" ? "완료" : "실행 중";
  return (
    <div className={`tool-card ${status}`}>
      <strong>{title}</strong> <span className="badge">{label}</span>
      {detail && <div className="detail">{detail}</div>}
    </div>
  );
}

function parse(result: string | undefined): Record<string, unknown> {
  try {
    return result ? JSON.parse(result) : {};
  } catch {
    return {};
  }
}

// AG-UI의 TOOL_CALL_START/ARGS/END/RESULT 이벤트가 오면 CopilotKit이 아래 render를 다시 부른다.
export function useToolStatusCards() {
  useRenderTool(
    {
      name: "analyze_document",
      agentId: AGENT_ID,
      parameters: z.object({ text: z.string() }),
      render: ({ status, result }) => {
        const data = parse(result) as { key_points?: string[]; issues?: string[] };
        const detail = status === "complete"
          ? `핵심 항목 ${data.key_points?.length ?? 0}개, 문제점 ${data.issues?.length ?? 0}개`
          : "문서를 분석하고 있습니다";
        return <StatusCard title="analyze_document" status={status} detail={detail} />;
      },
    },
    [],
  );

  useRenderTool(
    {
      name: "save_report",
      agentId: AGENT_ID,
      parameters: z.object({ title: z.string(), markdown: z.string() }),
      render: ({ status, parameters, result }) => {
        const path = parse(result).path as string | undefined;
        const detail = status === "complete" ? `저장: ${path ?? "-"}` : `"${parameters.title ?? ""}" 저장 중`;
        return <StatusCard title="save_report" status={status} detail={detail} />;
      },
    },
    [],
  );

  // 이름을 지정하지 않은 나머지 도구(read_document, list_documents, L12의 내 도구 등)
  useRenderTool(
    {
      name: "*",
      agentId: AGENT_ID,
      render: ({ name, status }) => <StatusCard title={name} status={status} />,
    },
    [],
  );
}
