# 기술적 지표 API

## 개요
기술적 지표 계산을 위한 API 모듈입니다.

## 주요 클래스

### TechnicalIndicator
기술적 지표 계산을 위한 메인 클래스입니다.

```python
class TechnicalIndicator:
    """
    기술적 지표 계산을 위한 클래스
    
    Attributes:
        data (pd.DataFrame): OHLCV 데이터
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): OHLCV 데이터프레임
        """
        self.data = data
```

## 주요 메서드

### 이동평균선
- `calculate_sma(period: int)`: 단순 이동평균선
- `calculate_ema(period: int)`: 지수 이동평균선
- `calculate_wma(period: int)`: 가중 이동평균선

### 모멘텀 지표
- `calculate_rsi(period: int)`: 상대강도지수
- `calculate_macd()`: 이동평균수렴확산지수
- `calculate_stochastic(period: int)`: 스토캐스틱

### 변동성 지표
- `calculate_bollinger_bands(period: int)`: 볼린저 밴드
- `calculate_atr(period: int)`: 평균진폭지수

## 사용 예시

```python
from technical_indicator import TechnicalIndicator

# 데이터 준비
data = pd.DataFrame(...)  # OHLCV 데이터

# 지표 계산기 초기화
indicator = TechnicalIndicator(data)

# RSI 계산
rsi = indicator.calculate_rsi(period=14)

# 볼린저 밴드 계산
bb_upper, bb_middle, bb_lower = indicator.calculate_bollinger_bands(period=20)
``` 