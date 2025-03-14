# 시각화 API

## 개요
기술적 지표와 시그널을 시각화하는 API 모듈입니다.

## 주요 클래스

### Visualizer
차트 시각화를 위한 메인 클래스입니다.

```python
class Visualizer:
    """
    차트 시각화를 위한 클래스
    
    Attributes:
        data (pd.DataFrame): OHLCV 데이터
        signals (pd.DataFrame): 시그널 데이터
    """
    
    def __init__(self, data: pd.DataFrame, signals: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): OHLCV 데이터프레임
            signals (pd.DataFrame): 시그널 데이터프레임
        """
        self.data = data
        self.signals = signals
```

## 주요 메서드

### 차트 시각화
- `plot_candlestick()`: 캔들스틱 차트
- `plot_volume()`: 거래량 차트
- `plot_indicator(name: str)`: 기술적 지표 차트

### 시그널 시각화
- `plot_signals()`: 매매 시그널 표시
- `plot_signal_heatmap()`: 시그널 히트맵
- `plot_signal_combination()`: 복합 시그널 시각화

## 사용 예시

```python
from visualizer import Visualizer

# 시각화 도구 초기화
visualizer = Visualizer(data, signals)

# 캔들스틱 차트 그리기
visualizer.plot_candlestick()

# RSI 지표 추가
visualizer.plot_indicator('RSI')

# 매매 시그널 표시
visualizer.plot_signals()

# 시그널 히트맵 생성
visualizer.plot_signal_heatmap()
``` 