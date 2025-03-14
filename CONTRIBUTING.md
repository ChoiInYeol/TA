# 기여 가이드라인

Technical Indicator Lamp 프로젝트에 기여하고 싶으신 분들을 환영합니다! 

## 기여 방법

1. **이슈 생성**
   - 버그를 발견하셨나요? 새로운 기능을 제안하고 싶으신가요?
   - 이슈 템플릿을 사용하여 상세한 내용을 작성해주세요.
   - 중복된 이슈가 없는지 먼저 확인해주세요.

2. **Pull Request 제출**
   - Fork 후 새로운 브랜치에서 작업해주세요.
   - 커밋 메시지는 명확하고 설명적으로 작성해주세요.
   - PR 설명에 관련된 이슈 번호를 포함해주세요.

## 개발 환경 설정

```bash
# 저장소 복제
git clone https://github.com/ChoiInYeol/technical-indicator-lamp.git
cd technical-indicator-lamp

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 코드 스타일

- Python 코드는 PEP 8 스타일 가이드를 따릅니다.
- Type hints를 사용해주세요.
- 함수와 클래스에 docstring을 작성해주세요.
- 테스트 코드를 작성해주세요.

## 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 리포트 생성
pytest --cov=src tests/
```

## 문서화

- 새로운 기능을 추가할 때는 문서도 함께 업데이트해주세요.
- 예제 코드는 실행 가능해야 합니다.
- 문서는 한글로 작성해주세요.

## 리뷰 프로세스

1. 자동화된 테스트가 통과해야 합니다.
2. 코드 리뷰어의 승인이 필요합니다.
3. 모든 코멘트가 해결되어야 합니다.

## 커밋 메시지 가이드라인

```
유형: 제목 (50자 이내)

본문 (선택사항, 72자마다 줄바꿈)

해결: #이슈번호
```

유형:
- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- style: 코드 포맷팅
- refactor: 코드 리팩토링
- test: 테스트 코드
- chore: 기타 변경사항

## 라이선스

이 프로젝트에 기여하는 것은 MIT 라이선스에 동의하는 것을 의미합니다. 