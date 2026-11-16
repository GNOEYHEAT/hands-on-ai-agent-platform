"""my_service_agent를 AG-UI 엔드포인트(http://localhost:8000/ag-ui)로 연다.

labs/07-copilotkit-frontend 화면은 고치지 않고 그대로 쓴다. 화면은 이 주소에 붙은 에이전트를
doc_report_agent라는 이름으로 부르지만, 실제로 답하는 것은 my_service_agent다.
labs/06-agui-backend/server.py와 같은 8000번 포트를 쓰므로 06 서버는 먼저 끈다.

    python labs/09-final-project/server.py
"""
import os
import sys
from pathlib import Path

import uvicorn
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent))
from my_service_agent.agent import root_agent  # noqa: E402

agui_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="my_service_app",
    user_id="demo_user",
    use_in_memory_services=True,
)

app = FastAPI(title="my_service_agent AG-UI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
add_adk_fastapi_endpoint(app, agui_agent, path="/ag-ui")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"AG-UI 엔드포인트: http://localhost:{port}/ag-ui (에이전트: {root_agent.name})")
    uvicorn.run(app, host="127.0.0.1", port=port)
