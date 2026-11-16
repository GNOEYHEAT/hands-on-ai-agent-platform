"""내 서비스의 도구(Function Tool). 아래 예시 도구를 내 아이디어에 맞는 도구로 바꾼다.

도구 함수를 만들 때 지킬 것:
- 인자와 반환값에 타입을 적는다(모델이 인자를 채우는 기준).
- docstring 첫 줄에 "언제 쓰는 도구인지"를 적는다(모델이 도구를 고르는 기준).
- {"status": "success" | "error", ...} 형태의 dict를 돌려준다.
"""
import re


# TODO(1): 이 예시 도구를 내 서비스의 도구로 바꾼다. 예) 리뷰 감성 분류, 일정 추출, 가격 비교
def extract_action_items(text: str) -> dict:
    """회의록·메모에서 할 일(TODO, ~해야 한다, ~까지)을 찾아 목록으로 돌려준다.

    Args:
        text: 분석할 회의록이나 메모 내용
    """
    pattern = re.compile(r"(TODO|해야|까지)")
    items = [line.strip("-* ").strip() for line in text.splitlines() if pattern.search(line)]
    return {"status": "success", "count": len(items), "action_items": items}
