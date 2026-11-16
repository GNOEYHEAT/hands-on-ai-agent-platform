"""L5 자동 검증: Goose가 만든 doc_stats.py(없으면 solution/doc_stats.py)를 샘플 문서로 실행해 출력 형식을 확인한다.

    python labs/02-goose-devenv/check.py              # 내 파일이 있으면 내 파일, 없으면 완성본
    python labs/02-goose-devenv/check.py --solution   # 항상 완성본
"""
import os, subprocess  # noqa: E401
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SAMPLE = ROOT / "data" / "samples" / "project_status_report.md"
REQUIRED = ("글자 수", "단어 수", "제목", "TODO", "위험", "지연", "# 스마트 배송 앱 프로젝트 주간 현황 보고")


def main() -> None:
    mine = HERE / "doc_stats.py"
    target = mine if mine.exists() and "--solution" not in sys.argv else HERE / "solution" / "doc_stats.py"
    print(f"검사 대상: {target.relative_to(ROOT).as_posix()}")
    res = subprocess.run([sys.executable, str(target), str(SAMPLE)], capture_output=True,
                         text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if res.returncode != 0:
        sys.exit(f"FAIL: 종료 코드 {res.returncode}\n{res.stdout}{res.stderr}")
    missing = [word for word in REQUIRED if word not in res.stdout]
    if missing:
        sys.exit(f"FAIL: 출력에 다음 항목이 없습니다: {missing}\n{res.stdout}")
    print(res.stdout.strip())
    print("CHECK OK")


if __name__ == "__main__":
    main()
