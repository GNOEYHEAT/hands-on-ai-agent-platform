"""AG-UI 엔드포인트에 RunAgentInput을 POST하고, 돌아오는 이벤트(SSE)를 한 줄씩 출력한다.

    python labs/06-agui-backend/send_run.py
    python labs/06-agui-backend/send_run.py --message "data/samples/meeting_notes.md 를 분석해 줘"
"""
import argparse
import json
import sys
import uuid

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(description="AG-UI 이벤트 스트림 관찰")
    parser.add_argument("--url", default="http://localhost:8000/ag-ui")
    parser.add_argument("--message", default="샘플 보고서를 분석해 줘")
    args = parser.parse_args()

    run_input = {                                   # AG-UI RunAgentInput
        "threadId": f"thread-{uuid.uuid4().hex[:8]}",
        "runId": f"run-{uuid.uuid4().hex[:8]}",
        "messages": [{"id": "msg-1", "role": "user", "content": args.message}],
        "state": {}, "tools": [], "context": [], "forwardedProps": {},
    }
    try:
        with httpx.stream("POST", args.url, json=run_input, timeout=120,
                          headers={"Accept": "text/event-stream"}) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith("data:"):
                    continue
                event = json.loads(line[5:])
                detail = event.get("toolCallName") or event.get("delta") or ""
                print(f"{event['type']:<22} {str(detail)[:60]!s}".rstrip().replace("\n", " "))
    except httpx.ConnectError:
        print(f"{args.url}에 연결하지 못했습니다. 다른 터미널에서 python labs/06-agui-backend/server.py 를 먼저 실행하세요.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
