"""문서 통계 스크립트(완성본). Goose에게 만들게 한 결과와 비교할 때 쓴다.

    python labs/02-goose-devenv/solution/doc_stats.py data/samples/project_status_report.md
"""
import sys
from pathlib import Path

KEYWORDS = ("TODO", "위험", "지연")


def main() -> int:
    if len(sys.argv) != 2:
        print("사용법: python doc_stats.py <문서 경로>")
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    print(f"파일: {path.name}")
    print(f"글자 수: {len(text)}")
    print(f"단어 수: {len(text.split())}")
    print("제목:")
    for line in text.splitlines():
        if line.startswith("#"):
            print(f"  {line}")
    print("키워드:")
    for keyword in KEYWORDS:
        print(f"  {keyword}: {text.count(keyword)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
