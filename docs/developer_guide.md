# 개발자 가이드

## 목차
1. [개발 환경 설정](#개발-환경-설정)
2. [프로젝트 구조](#프로젝트-구조)
3. [코드 스타일](#코드-스타일)
4. [테스트](#테스트)
5. [기여 가이드](#기여-가이드)
6. [배포](#배포)

## 프로젝트 구조

```
src/
├── config/                 # 설정 모듈
│   ├── __init__.py
│   ├── settings.py        # 기본 설정
│   ├── development.py     # 개발 환경 설정
│   └── production.py      # 운영 환경 설정
├── data/                  # 데이터 모듈
│   ├── raw/              # 원본 데이터
│   └── processed/        # 처리된 데이터
├── indicators/           # 기술적 지표 모듈
│   ├── __init__.py
│   └── technical_indicator.py
├── signals/             # 매매 시그널 모듈
│   ├── __init__.py
│   └── signal_generator.py
├── visualization/       # 시각화 모듈
│   ├── __init__.py
│   └── visualizer.py
└── main.py             # 메인 실행 모듈
```

## 개발 환경 설정

1. Poetry 설치:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 프로젝트 의존성 설치:
```bash
poetry install
```

3. 개발 환경 활성화:
```bash
poetry shell
```

## 코드 스타일

- PEP 8 준수
- 타입 힌트 사용
- 문서화 주석 필수
- 한글 주석 사용

## 테스트

### 단위 테스트 실행
```bash
pytest tests/
```

### 테스트 커버리지 확인
```bash
pytest --cov=src tests/
```

## 새로운 기능 추가

### 1. 기술적 지표 추가

1. `src/indicators/technical_indicator.py`에 새로운 지표 계산 메서드 추가
2. `src/config/settings.py`에 지표 설정 추가
3. `src/signals/signal_generator.py`에 시그널 생성 로직 추가

### 2. 매매 시그널 추가

1. `src/signals/signal_generator.py`에 새로운 시그널 생성 메서드 추가
2. 시그널 로직 문서화

### 3. 시각화 추가

1. `src/visualization/visualizer.py`에 새로운 시각화 메서드 추가
2. `src/config/settings.py`에 시각화 설정 추가

## 로깅

### 로그 레벨

- DEBUG: 개발 환경
- INFO: 운영 환경

### 로그 포맷

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 성능 최적화

### 데이터 처리

- pandas 벡터화 연산 사용
- 불필요한 복사 최소화
- 메모리 사용량 최적화

### 시각화

- matplotlib 스타일 최적화
- 데이터 캐싱
- 렌더링 성능 개선

## 배포

### 1. 버전 관리

- 시맨틱 버저닝 준수
- CHANGELOG.md 업데이트
- 태그 생성

### 2. 패키지 빌드

```bash
poetry build
```

### 3. 배포

```bash
poetry publish
```

## 문제 해결

### 디버깅

1. 로그 확인
2. 디버거 사용
3. 단위 테스트 실행

### 성능 프로파일링

```bash
python -m cProfile -o profile.stats run.py
snakeviz profile.stats
```

## 기여하기

1. 이슈 생성
2. 브랜치 생성
3. 코드 작성
4. 테스트 작성
5. PR 생성

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 