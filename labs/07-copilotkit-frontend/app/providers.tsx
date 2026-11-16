"use client";

import { CopilotKit } from "@copilotkit/react-core/v2";
import type { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  // runtimeUrl: 같은 Next.js 앱의 CopilotKit 런타임 경로(app/api/copilotkit)
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" enableInspector={false}>
      {children}
    </CopilotKit>
  );
}
