# Technical Indicator Lamp

![트레이딩 시그널 분석 대시보드](data/processed/trading_signals_heatmap.png)

## 프로젝트 개요

Technical Indicator Lamp는 다양한 기술적 지표를 활용하여 트레이딩 시그널을 생성하고 시각화하는 파이썬 기반 프로젝트입니다. 이 프로젝트는 모멘텀 지표와 반추세 지표를 포함한 다양한 기술적 지표를 계산하고, 이를 기반으로 매수/매도 신호를 생성하여 직관적인 히트맵 형태로 시각화합니다.

## 주요 기능

- **다양한 기술적 지표 계산**: SMA, EMA, MACD, RSI, 볼린저 밴드 등 20개 이상의 기술적 지표 계산
- **트레이딩 시그널 생성**: 각 기술적 지표에 기반한 매수/매도 신호 생성
- **시각적 대시보드**: 히트맵과 가격 차트를 결합한 직관적인 시각화 제공
- **거래일 기반 분석**: 실제 거래일을 기준으로 데이터 처리 및 분석

## 프로젝트 구조

```
.
├─data
│  ├─processed        # 처리된 데이터 파일
│  └─raw              # 원본 데이터 파일
├─output              # 분석 결과 출력
│  └─figures          # 생성된 그래프 및 시각화
└─src                 # 소스 코드
```

## 주요 모듈

### 1. 기술적 지표 계산 (`technical_indicator.py`)

두 가지 주요 클래스로 구성됩니다:

- **CORE16MomentumIndicator**: 추세 추종형 지표 계산
  - SMA, EMA, MACD, Parabolic SAR, ADX, Aroon 등
- **CORE16ContrarianIndicator**: 반추세형 지표 계산
  - RSI, 볼린저 밴드, CCI, 스토캐스틱, Williams %R 등

### 2. 시그널 생성 (`signal_generator.py`)

`SignalGenerator` 클래스는 계산된 기술적 지표를 기반으로 트레이딩 시그널을 생성합니다:

- 모멘텀 기반 신호 (추세 추종)
- 반추세 기반 신호 (과매수/과매도)
- 각 신호의 성과 측정 및 분석

### 3. 시각화 (`visualizer.py`)

`signal_heatmap_with_price` 함수는 생성된 시그널을 히트맵으로 시각화하고, 가격 데이터와 함께 표시합니다:

- 히트맵으로 각 지표별 매수/매도 신호 표시
- 가격 차트와 시그널 정렬
- 날짜별 시그널 패턴 분석 용이

### 4. 메인 실행 (`main.py`)

전체 워크플로우를 실행하는 메인 모듈:

- 데이터 로드
- 기술적 지표 계산
- 시그널 생성
- 결과 저장 및 시각화

## 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/ChoiInYeol/technical-indicator-lamp.git
cd technical-indicator-lamp
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

1. 데이터 준비:
   - `data/raw` 디렉토리에 OHLCV 형식의 CSV 파일 준비

2. 메인 스크립트 실행:
```bash
python src/main.py
```

3. 시각화 실행:
```bash
python src/visualizer.py
```

## 사용 예제

### 예제 1: 기본 분석 실행

```python
# main.py 실행 예제
import pandas as pd
from technical_indicator import CORE16MomentumIndicator, CORE16ContrarianIndicator
from signal_generator import SignalGenerator

# 데이터 로드
data = pd.read_csv('data/raw/spy_data.csv', index_col='Date', parse_dates=True)

# 기술적 지표 계산
momentum_indicator = CORE16MomentumIndicator(data, resample='1d')
contrarian_indicator = CORE16ContrarianIndicator(data, resample='1d')

# 지표 계산
momentum_df = momentum_indicator.calculate_all_indicators()
contrarian_df = contrarian_indicator.calculate_all_indicators()

# 신호 생성
signal_generator = SignalGenerator(pd.concat([data, momentum_df, contrarian_df], axis=1))
momentum_signals = signal_generator.generate_momentum_signals()
contrarian_signals = signal_generator.generate_contrarian_signals()

# 결과 저장
all_signals = pd.concat([momentum_signals, contrarian_signals], axis=1)
all_signals.to_csv('data/processed/trading_signals.csv')
```

### 예제 2: 시각화 실행

```python
# visualizer.py 실행 예제
from visualizer import signal_heatmap_with_price

# 최근 30일 거래일 기준 시각화
signal_heatmap_with_price(
    signal_file="data/processed/trading_signals.csv",
    price_file="data/raw/spy_data.csv",
    last_n_trading_days=30,
    annot_size=8,
    square=True,
    savefig="data/processed/trading_signals_heatmap.png"
)
```

## 결과물

아래는 생성된 트레이딩 시그널 히트맵의 예시입니다:

![트레이딩 시그널 분석 대시보드](data/processed/trading_signals_heatmap.png)

이 히트맵은 다양한 기술적 지표에서 생성된 매수/매도 신호를 시각적으로 표현하며, 하단의 가격 차트와 함께 시장 상황을 종합적으로 분석할 수 있게 해줍니다.

## 시그널 해석 방법

- **녹색 셀(Buy)**: 매수 신호
- **빨간색 셀(Sell)**: 매도 신호
- **회색 셀(Neu)**: 중립 신호
- **빈 셀**: 신호 없음

## 지원하는 기술적 지표

### 모멘텀 지표
- SMA (단순이동평균)
- EMA (지수이동평균)
- TSI (True Strength Index)
- MACD (Moving Average Convergence Divergence)
- PSAR (Parabolic SAR)
- ADX (Average Directional Index)
- Aroon
- ADL (Accumulation Distribution Line)
- ADR (Average Daily Range)
- Ichimoku Cloud
- Keltner Channel

### 반추세 지표
- RSI (Relative Strength Index)
- Bollinger Bands
- CCI (Commodity Channel Index)
- Stochastic Oscillator
- Williams %R
- CMO (Chande Momentum Oscillator)
- DeMarker
- Donchian Channel
- Pivot Points
- PSY (Psychological Line)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여자

- Tommy Lee
- Joon Kim
- Inyeol Choi

## 참고 문헌

- Technical Analysis of the Financial Markets - John J. Murphy
- Technical Indicators and Trading Strategies - Tushar Chande 