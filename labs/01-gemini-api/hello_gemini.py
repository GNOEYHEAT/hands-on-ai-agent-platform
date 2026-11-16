"""L1·L4 Gemini API 첫 호출: 샘플 문서를 3줄로 요약한다.

    python labs/01-gemini-api/hello_gemini.py           # 실제 호출(.env의 GOOGLE_API_KEY 필요)
    python labs/01-gemini-api/hello_gemini.py --mock    # 키 없이 모의 응답으로 흐름만 확인
    python labs/01-gemini-api/hello_gemini.py --legacy  # 레거시 generateContent 경로로 호출
"""
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]          # 저장소 최상위
load_dotenv(ROOT / ".env")                           # GOOGLE_API_KEY, DOC_AGENT_MODEL을 읽는다

MODEL_ID = os.getenv("DOC_AGENT_MODEL", "gemini-3.5-flash-lite")
DOC_PATH = ROOT / "data" / "samples" / "project_status_report.md"
PROMPT = "다음 문서를 한국어 3줄로 요약해 줘. 각 줄은 '- '로 시작해.\n\n"


def summarize(text: str) -> str:
    """Interactions API(신규 권장)로 요약을 요청한다."""
    from google import genai

    client = genai.Client()  # 환경 변수 GOOGLE_API_KEY를 읽는다
    interaction = client.interactions.create(model=MODEL_ID, input=PROMPT + text)
    return interaction.output_text


def summarize_legacy(text: str) -> str:
    """generateContent(레거시, 계속 지원)로 같은 요청을 보낸다."""
    from google import genai

    client = genai.Client()
    response = client.models.generate_content(model=MODEL_ID, contents=PROMPT + text)
    return response.text


def mock_summary(text: str) -> str:
    """키 없이 흐름을 확인하는 모의 응답: 문서의 첫 글머리 세 줄을 돌려준다."""
    bullets = [line.strip() for line in text.splitlines() if line.strip().startswith("- ")]
    return "\n".join(bullets[:3])


def main() -> int:
    parser = argparse.ArgumentParser(description="Gemini API로 샘플 문서를 요약한다")
    parser.add_argument("--mock", action="store_true", help="API를 부르지 않고 모의 응답을 쓴다")
    parser.add_argument("--legacy", action="store_true", help="generateContent API로 호출한다")
    args = parser.parse_args()

    text = DOC_PATH.read_text(encoding="utf-8")
    use_mock = args.mock or MODEL_ID == "mock"

    if use_mock:
        model_label = "gemini-3.5-flash-lite" if MODEL_ID == "mock" else MODEL_ID
        print(f"모델 ID: {model_label} (모의 응답, API 호출 없음)")
        print(f"문서: data/samples/{DOC_PATH.name}")
        print("요약:")
        print(mock_summary(text))
        return 0

    if not os.getenv("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY가 없습니다. .env.example을 .env로 복사하고 키를 넣은 뒤 다시 실행하세요.")
        print("키 없이 흐름만 보려면: python labs/01-gemini-api/hello_gemini.py --mock")
        return 2

    from google.genai import errors

    try:
        summary = summarize_legacy(text) if args.legacy else summarize(text)
    except errors.APIError as exc:
        print(f"Gemini API 오류 {exc.code}: {exc.message}")
        if exc.code == 429:
            print("무료 등급 사용량 제한에 걸렸습니다. 잠시 뒤 다시 시도하거나 AI Studio에서 한도를 확인하세요.")
        elif exc.code == 404:
            print(f"모델 ID '{MODEL_ID}'를 찾지 못했습니다. list_models.py로 사용 가능한 ID를 확인하세요.")
        return 1

    print(f"모델 ID: {MODEL_ID} ({'generateContent' if args.legacy else 'Interactions API'})")
    print(f"문서: data/samples/{DOC_PATH.name}")
    print("요약:")
    print(summary.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
