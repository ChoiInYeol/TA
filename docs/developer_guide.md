# Technical Indicator Lamp 개발자 가이드

## 목차
1. [개발 환경 설정](#개발-환경-설정)
2. [프로젝트 구조](#프로젝트-구조)
3. [코드 스타일](#코드-스타일)
4. [테스트](#테스트)
5. [기여 가이드](#기여-가이드)
6. [배포](#배포)

## 개발 환경 설정

### 필수 요구사항
- Python 3.11 이상
- Git
- 가상 환경 관리자 (venv, conda 등)

### 개발 환경 구성
```bash
# 1. 저장소 클론 및 브랜치 생성
git clone https://github.com/ChoiInYeol/technical-indicator-lamp.git
cd technical-indicator-lamp
git checkout -b feature/your-feature-name

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 개발 의존성 설치
pip install -r requirements.txt

# 4. pre-commit 설정
pre-commit install
```

## 프로젝트 구조
```
technical-indicator-lamp/
├── .github/
│   └── workflows/          # GitHub Actions 워크플로우
├── data/
│   ├── raw/               # 원본 데이터
│   └── processed/         # 처리된 데이터
├── docs/                  # 문서
├── output/
│   └── figures/          # 생성된 시각화
├── src/                  # 소스 코드
│   ├── technical_indicator.py
│   ├── signal_generator.py
│   └── visualizer.py
├── tests/                # 테스트 코드
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.cfg            # 개발 도구 설정
```

## 코드 스타일

### Python 코딩 표준
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) 준수
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) 참고

### 코드 포맷팅
```bash
# Black으로 코드 포맷팅
black src tests

# isort로 import 정렬
isort src tests
```

### 린팅
```bash
# Flake8로 코드 검사
flake8 src tests

# mypy로 타입 검사
mypy src tests
```

### 문서화
- 모든 모듈, 클래스, 함수에 독스트링 작성
- Type hints 사용
- 복잡한 로직에 인라인 주석 추가

예시:
```python
def calculate_indicator(data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """기술적 지표 계산

    Args:
        data (pd.DataFrame): OHLCV 데이터
        window (int, optional): 계산 기간. 기본값 20

    Returns:
        pd.DataFrame: 계산된 지표 값

    Raises:
        ValueError: 입력 데이터가 비어있는 경우
    """
```

## 테스트

### 테스트 실행
```bash
# 전체 테스트 실행
pytest

# 커버리지 리포트 생성
pytest --cov=src --cov-report=html
```

### 테스트 작성 가이드
1. **테스트 구조**
   - `tests/conftest.py`: 공통 fixture 정의
   - `tests/test_*.py`: 모듈별 테스트

2. **테스트 케이스 작성**
   ```python
   def test_indicator_calculation(sample_data):
       """지표 계산 테스트"""
       # Given
       indicator = TechnicalIndicator(sample_data)
       
       # When
       result = indicator.calculate()
       
       # Then
       assert not result.empty
       assert all(result.columns == expected_columns)
   ```

3. **테스트 커버리지**
   - 코드 커버리지 80% 이상 유지
   - 주요 기능 및 엣지 케이스 테스트

## 기여 가이드

### 기여 절차
1. Issue 생성 또는 기존 Issue 선택
2. Fork 및 브랜치 생성
3. 코드 작성 및 테스트
4. Pull Request 생성

### Pull Request 체크리스트
- [ ] 코드 스타일 준수
- [ ] 테스트 추가/수정
- [ ] 문서 업데이트
- [ ] 변경사항 설명

### 커밋 메시지 규칙
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 기타 변경사항
```

## 배포

### 버전 관리
- [Semantic Versioning](https://semver.org/) 사용
- `MAJOR.MINOR.PATCH` 형식

### 릴리스 절차
1. 버전 업데이트
2. CHANGELOG.md 업데이트
3. 릴리스 노트 작성
4. 태그 생성 및 푸시

### 자동화된 배포
GitHub Actions를 통해 다음 작업이 자동화됩니다:
1. 코드 품질 검사
2. 테스트 실행
3. 문서 생성
4. 패키지 배포 (해당하는 경우) 