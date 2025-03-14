"""
프로젝트 설정 파일
"""
from pathlib import Path

# 프로젝트 경로 설정
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = PROJECT_ROOT / 'output'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# 데이터 파일 경로
SPY_DATA_FILE = RAW_DATA_DIR / 'spy_data.csv'
SIGNALS_FILE = PROCESSED_DATA_DIR / 'trading_signals.csv'
INDICATORS_FILE = PROCESSED_DATA_DIR / 'combined_indicators.csv'
HEATMAP_FILE = FIGURES_DIR / 'trading_signals_heatmap.png'

# 데이터 수집 설정
TRADING_START_TIME = "21:30:00"  # 한국 시간 기준 다음날 아침 6:30
DATA_START_DATE = "2000-01-01"

# 기술적 지표 설정
MOMENTUM_INDICATORS = {
    'SMA': {'window_size': 20},
    'EMA': {'window_size': 20},
    'TSI': {'short_window': 2, 'long_window': 20},
    'MACD': {'short_window': 12, 'long_window': 26, 'signal_window': 9},
    'PSAR': {'acceleration': 0.02, 'max_acceleration': 0.2},
    'ADX': {'window_size': 20},
    'Aroon': {'window_size': 20},
    'ADL': {'window_size': 20},
    'ADR': {'window_size': 20},
    'Ichimoku': {'kijun': 26, 'senkou': 52, 'tenkan': 9},
    'Keltner': {'window_size': 20}
}

CONTRARIAN_INDICATORS = {
    'RSI': {'window_size': 14, 'overbought': 70, 'oversold': 30},
    'BB': {'window_size': 20, 'num_std': 2},
    'CCI': {'window_size': 20},
    'Stoch': {'k_window': 14, 'd_window': 3},
    'Williams': {'window_size': 14},
    'CMO': {'window_size': 14},
    'DeMarker': {'window_size': 14},
    'Donchian': {'window_size': 20},
    'Pivot': {'scale': 2.0},
    'PSY': {'window_size': 12},
    'NPSY': {'window_size': 12}
}

# 시각화 설정
VISUALIZATION = {
    'figure_size': (15, 10),
    'dpi': 300,
    'colors': {
        'buy': '#4dff4d',
        'sell': '#ff4d4d',
        'neutral': '#e6e6e6'
    }
}

# 로깅 설정
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO' 