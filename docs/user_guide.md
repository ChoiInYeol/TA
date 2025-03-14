# 사용자 가이드

## 소개

이 프로젝트는 기술적 지표를 계산하고 매매 시그널을 생성하는 도구입니다.

## 설치

1. Poetry를 사용한 설치:
```bash
poetry install
```

2. 가상 환경 활성화:
```bash
poetry shell
```

## 사용 방법

### 기본 실행

프로젝트를 실행하려면 다음 명령어를 사용합니다:
```bash
python run.py
```

### 환경 설정

환경 변수를 통해 실행 환경을 설정할 수 있습니다:

```bash
# 개발 환경
export TA_ENV=development

# 운영 환경
export TA_ENV=production
```

### 출력 파일

프로젝트는 다음과 같은 출력 파일을 생성합니다:

- `src/data/processed/indicators.csv`: 계산된 기술적 지표
- `src/data/processed/signals.csv`: 생성된 매매 시그널
- `src/data/processed/heatmap.png`: 시각화된 대시보드

## 기술적 지표

### 모멘텀 지표

- SMA (단순 이동평균)
- EMA (지수 이동평균)
- TSI (True Strength Index)
- MACD (Moving Average Convergence Divergence)
- PSAR (Parabolic SAR)
- ADX (Average Directional Index)
- Aroon
- ADL (Accumulation/Distribution Line)
- ADR (Advance/Decline Ratio)
- Ichimoku (일목균형표)
- Keltner Channel

### 반대매매 지표

- RSI (Relative Strength Index)
- BB (Bollinger Bands)
- CCI (Commodity Channel Index)
- Stochastic Oscillator
- Williams %R
- CMO (Chande Momentum Oscillator)
- DeMarker
- Donchian Channel
- Pivot Points
- PSY (Psychological Line)
- NPSY (Negative Psychological Line)

## 매매 시그널

매매 시그널은 다음과 같은 의미를 가집니다:

- 1: 매수 시그널
- -1: 매도 시그널
- 0: 중립 시그널

## 대시보드

대시보드는 다음 정보를 포함합니다:

1. 매매 시그널 히트맵
   - 빨간색: 매도 시그널
   - 회색: 중립 시그널
   - 초록색: 매수 시그널

2. 캔들차트
   - 빨간색: 상승
   - 초록색: 하락

3. 거래량 차트
   - 빨간색: 상승 거래량
   - 파란색: 하락 거래량

## 문제 해결

### 로그 확인

로그 파일은 `logs/app.log`에 저장됩니다.

### 디버그 모드

개발 환경에서는 자동으로 디버그 모드가 활성화됩니다.

## 지원

문제가 발생하면 이슈를 생성해주세요. 