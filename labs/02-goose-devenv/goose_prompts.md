# Goose에게 줄 프롬프트

Goose 채팅 창에 아래 문장을 차례대로 붙여 넣는다. Goose가 파일을 만들거나 명령을 실행하기 전에 무엇을 하려는지 읽고 확인한다.

## 1. 문서 읽기

```
data/samples/project_status_report.md 파일을 읽고 어떤 문서인지 세 문장으로 설명해 줘.
```

## 2. 통계 스크립트 만들기

```
labs/02-goose-devenv/doc_stats.py 파일을 만들어 줘.
- 명령줄 인자로 받은 문서 경로를 UTF-8로 읽는다.
- 다음 순서로 출력한다:
  파일: <파일 이름>
  글자 수: <숫자>
  단어 수: <공백으로 나눈 단어 수>
  제목:
    <'#'으로 시작하는 줄을 그대로 한 줄씩>
  키워드:
    TODO: <등장 횟수>
    위험: <등장 횟수>
    지연: <등장 횟수>
- 표준 라이브러리만 쓴다.
```

## 3. 실행하고 확인하기

```
python labs/02-goose-devenv/doc_stats.py data/samples/project_status_report.md 를 실행하고 결과를 보여 줘.
그다음 python labs/02-goose-devenv/check.py 를 실행해서 CHECK OK가 나오는지 확인해 줘.
```

## 4. (확장) 고쳐 달라고 하기

```
doc_stats.py에 문장 수(마침표 기준)를 추가하고, 기존 출력 형식은 그대로 유지해 줘.
```
