# Technical Indicator Lamp 사용자 가이드

## 목차
1. [소개](#소개)
2. [설치 방법](#설치-방법)
3. [사용 방법](#사용-방법)
4. [기술적 지표](#기술적-지표)
5. [시그널 해석](#시그널-해석)
6. [시각화](#시각화)
7. [자동화](#자동화)
8. [문제 해결](#문제-해결)

## 소개
Technical Indicator Lamp는 S&P 500 지수의 기술적 분석을 자동화하는 도구입니다. 다양한 기술적 지표를 계산하고, 트레이딩 시그널을 생성하며, 이를 시각적으로 표현합니다.

## 설치 방법
```bash
# 1. 저장소 클론
git clone https://github.com/ChoiInYeol/technical-indicator-lamp.git
cd technical-indicator-lamp

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt
```

## 사용 방법
### 기본 사용
```python
# 데이터 분석 실행
python src/main.py
```

### 수동 실행 옵션
```python
from src.technical_indicator import CORE16MomentumIndicator, CORE16ContrarianIndicator
from src.signal_generator import SignalGenerator
from src.visualizer import aligned_signal_candlestick

# 1. 데이터 로드
data = pd.read_csv('data/raw/spy_data.csv', index_col='Date', parse_dates=True)

# 2. 기술적 지표 계산
momentum = CORE16MomentumIndicator(data)
contrarian = CORE16ContrarianIndicator(data)

momentum_indicators = momentum.calculate_all_indicators()
contrarian_indicators = contrarian.calculate_all_indicators()

# 3. 시그널 생성
generator = SignalGenerator(data)
signals = generator.generate_all_signals()

# 4. 시각화
aligned_signal_candlestick(
    signal_file='data/processed/trading_signals.csv',
    price_file='data/raw/spy_data.csv',
    last_n_trading_days=30
)
```

## 기술적 지표
### 모멘텀 지표
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- MACD (Moving Average Convergence Divergence)
- TSI (True Strength Index)
- ADX (Average Directional Index)
- Aroon
- Ichimoku Cloud
- Keltner Channel

### 반추세 지표
- RSI (Relative Strength Index)
- BB (Bollinger Bands)
- CCI (Commodity Channel Index)
- Stochastic
- Williams %R
- CMO (Chande Momentum Oscillator)
- DeMarker
- PSY (Psychology Line)

## 시그널 해석
- 🟩 매수 시그널 (1): 상승 추세 또는 과매도 상태
- ⬜️ 중립 시그널 (0): 명확한 추세 없음
- 🟥 매도 시그널 (-1): 하락 추세 또는 과매수 상태

## 시각화
### 히트맵
- 상단: 기술적 지표별 시그널 히트맵
- 중단: 캔들스틱 차트
- 하단: 거래량 차트

### 설정 옵션
```python
aligned_signal_candlestick(
    signal_file='signals.csv',
    price_file='prices.csv',
    last_n_trading_days=30,  # 표시할 거래일 수
    savefig='output.png'     # 저장할 파일 경로
)
```

## 자동화
GitHub Actions를 통해 다음 작업이 자동으로 실행됩니다:
1. 매일 오전 6:30 (한국 시간) 데이터 업데이트
2. 기술적 지표 계산
3. 시그널 생성
4. 시각화 생성
5. 결과물 저장 및 커밋

## 문제 해결
### 일반적인 문제
1. 데이터 로드 실패
   - 인터넷 연결 확인
   - yfinance API 상태 확인

2. 시각화 오류
   - 필요한 데이터 파일 존재 여부 확인
   - 데이터 형식 확인

3. 자동화 실패
   - GitHub Actions 로그 확인
   - 저장소 권한 설정 확인

### 로그 확인
- 애플리케이션 로그: `src/main.log`
- 데이터 수집 로그: `data/raw/spy_data.log`

### 지원
문제가 지속되면 다음 방법으로 도움을 받을 수 있습니다:
1. GitHub Issues 생성
2. 로그 파일 첨부
3. 발생 상황 상세 설명 