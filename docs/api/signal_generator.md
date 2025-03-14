# 시그널 생성기 API

## 개요
기술적 지표를 기반으로 매수/매도 시그널을 생성하는 API 모듈입니다.

## 주요 클래스

### SignalGenerator
매매 시그널 생성을 위한 메인 클래스입니다.

```python
class SignalGenerator:
    """
    매매 시그널 생성을 위한 클래스
    
    Attributes:
        indicator (TechnicalIndicator): 기술적 지표 계산기
        signals (pd.DataFrame): 생성된 시그널 데이터
    """
    
    def __init__(self, indicator: TechnicalIndicator):
        """
        Args:
            indicator (TechnicalIndicator): 기술적 지표 계산기 인스턴스
        """
        self.indicator = indicator
        self.signals = pd.DataFrame()
```

## 주요 메서드

### 단일 지표 시그널
- `generate_rsi_signals(period: int, overbought: float, oversold: float)`: RSI 기반 시그널
- `generate_macd_signals()`: MACD 기반 시그널
- `generate_bollinger_signals(period: int)`: 볼린저 밴드 기반 시그널

### 복합 시그널
- `combine_signals(signal_list: List[str])`: 여러 시그널 조합
- `weight_signals(weights: Dict[str, float])`: 시그널 가중치 적용

## 사용 예시

```python
from signal_generator import SignalGenerator

# 시그널 생성기 초기화
generator = SignalGenerator(indicator)

# RSI 시그널 생성
rsi_signals = generator.generate_rsi_signals(
    period=14,
    overbought=70,
    oversold=30
)

# MACD 시그널 생성
macd_signals = generator.generate_macd_signals()

# 시그널 조합
combined_signals = generator.combine_signals(['RSI', 'MACD'])
``` 