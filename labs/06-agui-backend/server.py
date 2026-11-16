"""doc_report_agent를 AG-UI 엔드포인트(http://localhost:8000/ag-ui)로 여는 Backend 서버.

    python labs/06-agui-backend/server.py
"""
import os
import sys
from pathlib import Path

import uvicorn
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doc_report_agent.agent import root_agent  # noqa: E402

# ADK 에이전트를 AG-UI 규격으로 감싼다. 세션은 메모리에 둔다(서버를 끄면 사라진다).
agui_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="doc_report_app",
    user_id="demo_user",
    use_in_memory_services=True,
)

app = FastAPI(title="doc_report_agent AG-UI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # Frontend 출처만 허용(SEC-11)
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
add_adk_fastapi_endpoint(app, agui_agent, path="/ag-ui")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"AG-UI 엔드포인트: http://localhost:{port}/ag-ui (모델: {os.getenv('DOC_AGENT_MODEL', 'gemini-3.5-flash-lite')})")
    uvicorn.run(app, host="127.0.0.1", port=port)
