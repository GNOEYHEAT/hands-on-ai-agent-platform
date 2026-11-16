"""L4 모델 목록에서 DOC_AGENT_MODEL(기본 gemini-3.5-flash-lite)을 쓸 수 있는지 확인한다.

    python labs/01-gemini-api/list_models.py           # 실제 조회(.env의 GOOGLE_API_KEY 필요)
    python labs/01-gemini-api/list_models.py --mock    # 키 없이 모의 목록으로 확인
"""
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

MODEL_ID = os.getenv("DOC_AGENT_MODEL", "gemini-3.5-flash-lite")
MOCK_MODELS = ["models/gemini-3.5-flash-lite", "models/gemini-3.1-flash-lite", "models/gemini-2.5-flash-lite"]


def fetch_model_names() -> list[str]:
    from google import genai

    client = genai.Client()
    return [model.name for model in client.models.list()]


def main() -> int:
    parser = argparse.ArgumentParser(description="사용 가능한 Gemini 모델 ID를 확인한다")
    parser.add_argument("--mock", action="store_true", help="API를 부르지 않고 모의 목록을 쓴다")
    args = parser.parse_args()

    target = "gemini-3.5-flash-lite" if MODEL_ID == "mock" else MODEL_ID
    if args.mock or MODEL_ID == "mock":
        names = MOCK_MODELS
        print("(모의 목록, API 호출 없음)")
    elif not os.getenv("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY가 없습니다. .env.example을 .env로 복사하고 키를 넣은 뒤 다시 실행하세요.")
        print("키 없이 흐름만 보려면: python labs/01-gemini-api/list_models.py --mock")
        return 2
    else:
        names = fetch_model_names()

    short = [name.removeprefix("models/") for name in names]
    print("flash-lite 계열 모델:")
    for name in short:
        if "flash-lite" in name:
            print(f"  {name}")
    status = "available" if target in short else "not found"
    print(f"{target}: {status}")
    return 0 if status == "available" else 1


if __name__ == "__main__":
    sys.exit(main())
