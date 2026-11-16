# L1·L4 Gemini API 연결 확인 / 첫 호출

이 실습에서는 Python 코드로 Gemini API를 처음 불러 봅니다. Gemini API는 Google의 Gemini 모델을 프로그램에서 불러 쓸 수 있게 열어 둔 창구입니다. `google-genai` SDK(Gemini API를 Python에서 쉽게 부르도록 Google이 만든 라이브러리)로 모델 목록에 `gemini-3.5-flash-lite`가 있는지 확인하고, 샘플 문서를 요약해 달라고 요청합니다.

- L1은 basic 트랙의 실습 1입니다. `hello_gemini.py`만 실행합니다.
- L4는 advanced 트랙의 실습 4입니다. 두 스크립트를 모두 실행합니다.

## 준비

API 키는 Gemini API를 부를 권한이 있다는 것을 증명하는 비밀 문자열입니다. 코드에 직접 적지 않고 `.env` 파일에 넣어 둡니다. `.env`는 프로그램이 읽어 갈 설정 값(환경 변수)을 적어 두는 파일입니다.

1. 최상위 README의 [2. API 키 등록](../../README.md#2-api-키-등록)대로 저장소 최상위 폴더(`labs`, `data`가 보이는 폴더)에서 `.env.example`을 복사해 `.env`를 만드세요.
2. `.env`를 편집기로 열고 `GOOGLE_API_KEY=` 뒤에 Google AI Studio에서 받은 키를 넣으세요. 값에는 따옴표를 붙이지 않습니다. 다 채우면 키와 모델 ID 줄이 아래처럼 됩니다(`발급받은-키` 자리에 실제 키).

```
GOOGLE_API_KEY=발급받은-키
DOC_AGENT_MODEL=gemini-3.5-flash-lite
```

## 실행

터미널(명령을 글자로 입력해 실행하는 창)에서 진행합니다. 반드시 가상환경을 활성화한(입력줄 앞에 `(.venv)`가 보이는) 터미널을 쓰세요. 가상환경은 이 강의에 필요한 패키지를 다른 프로젝트와 섞이지 않게 따로 담아 두는 폴더입니다. 모든 명령은 저장소 최상위 폴더에서 입력하세요.

1. 모델 목록에 기본 모델이 있는지 확인하세요.

   ```
   python labs/01-gemini-api/list_models.py
   ```

2. 샘플 문서 요약을 요청하세요.

   ```
   python labs/01-gemini-api/hello_gemini.py
   ```

3. 자동 확인을 실행하세요. 마지막 줄에 `CHECK OK`가 나오면 성공입니다.

   ```
   python labs/01-gemini-api/check.py
   ```

각 스크립트가 하는 일은 다음과 같습니다.

- `list_models.py`: `client.models.list()`로 받은 목록에 `DOC_AGENT_MODEL`이 있는지 확인하고, `gemini-3.5-flash-lite: available`처럼 출력합니다.
- `hello_gemini.py`: Interactions API(`client.interactions.create`)로 `data/samples/project_status_report.md`를 3줄로 요약해 받습니다. Interactions API는 Google이 새 프로젝트에 권장하는 호출 방식입니다. `--legacy`를 붙이면 예전 방식인 `generateContent`(`client.models.generate_content`)로 같은 요청을 보냅니다. 예전 방식도 계속 지원됩니다.

## 키 없이 해 보기(모의 응답)

API 키가 아직 없어도 흐름은 확인할 수 있습니다. 모의 응답은 API를 부르지 않고 미리 정해 둔 답을 보여 주는 방식입니다.

```
python labs/01-gemini-api/hello_gemini.py --mock
```

```
모델 ID: gemini-3.5-flash-lite (모의 응답, API 호출 없음)
문서: data/samples/project_status_report.md
요약:
- 전체 진행률은 62%로 계획(70%)보다 8%p 낮다.
- 주문 조회 화면과 배송 추적 API 개발을 마쳤다.
- 결제 연동은 외부 PG사 테스트 계정 발급이 늦어져 지연되고 있다.
```

모의 응답은 문서의 첫 글머리 세 줄을 그대로 보여 줄 뿐입니다. 모델이 요약한 결과가 아닙니다. `check.py`는 기본으로 이 모의 경로를 검사합니다. 키를 넣은 뒤에는 `python labs/01-gemini-api/check.py --live`로 실제 호출까지 검사할 수 있습니다.

## 막히면

| 화면에 보이는 것 | 원인과 해결 |
| --- | --- |
| `GOOGLE_API_KEY가 없습니다` (종료 코드 2) | `.env`가 저장소 최상위에 없거나 키 줄이 비어 있습니다. 위 "준비"를 다시 확인하세요 |
| `Gemini API 오류 429` | 무료 등급 사용량 제한에 걸렸습니다. 잠시 뒤 다시 하거나 AI Studio에서 한도를 확인하세요 |
| `Gemini API 오류 404` | 모델 ID에 오타가 있습니다. `list_models.py`로 사용 가능한 ID를 확인하고 `.env`의 `DOC_AGENT_MODEL`을 고치세요 |
| `ModuleNotFoundError: google` | 가상환경이 활성화되어 있지 않습니다. 가상환경을 활성화한 뒤 다시 실행하세요 |
