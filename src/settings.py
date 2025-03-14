"""
기본 설정 모듈

이 모듈은 프로젝트의 기본 설정을 정의합니다.
"""

import logging
from pathlib import Path
from typing import Any, Dict

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent

# 디렉토리 설정
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

# 디렉토리 생성
for directory in [DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 파일 경로 설정
LOG_FILE = LOG_DIR / "technical_analysis.log"
SPY_DATA_FILE = DATA_DIR / "spy_data.csv"
INDICATORS_FILE = PROCESSED_DATA_DIR / "indicators.csv"
SIGNALS_FILE = PROCESSED_DATA_DIR / "signals.csv"
HEATMAP_FILE = PROCESSED_DATA_DIR / "dashboard.png"
DASHBOARD_FILE = PROCESSED_DATA_DIR / "dashboard.html"

# 로깅 설정
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_LEVEL = logging.INFO

# 기술적 지표 설정
TECHNICAL_INDICATORS: Dict[str, Any] = {
    "모멘텀 지표": {
        "SMA": {
            "periods": [20, 50],  # 단순 이동평균 기간
        },
        "EMA": {
            "periods": [20, 50],  # 지수 이동평균 기간
        },
        "TSI": {
            "short_period": 13,  # 단기 기간
            "long_period": 25,  # 장기 기간
        },
        "MACD": {
            "short_period": 12,  # 단기 기간
            "long_period": 26,  # 장기 기간
            "signal_period": 9,  # 시그널 기간
        },
        "PSAR": {
            "af_start": 0.02,  # 가속도 시작값
            "af_increment": 0.02,  # 가속도 증가값
            "af_max": 0.2,  # 최대 가속도
        },
        "ADX": {
            "period": 14,  # 기간
        },
        "Aroon": {
            "period": 14,  # 기간
        },
        "ADL": {
            "period": 20,  # 기간
        },
        "ADR": {
            "period": 20,  # 기간
        },
        "Ichimoku": {
            "tenkan_period": 9,  # 전환선 기간
            "kijun_period": 26,  # 기준선 기간
        },
        "Keltner": {
            "period": 20,  # 기간
            "multiplier": 2.0,  # 승수
        },
    },
    "반대매매 지표": {
        "RSI": {
            "period": 14,  # 기간
        },
        "BB": {
            "period": 20,  # 기간
            "std_dev": 2.0,  # 표준편차
        },
        "CCI": {
            "period": 20,  # 기간
        },
        "Stoch": {
            "k_period": 14,  # %K 기간
            "d_period": 3,  # %D 기간
        },
        "Williams": {
            "period": 14,  # 기간
        },
        "CMO": {
            "period": 14,  # 기간
        },
        "DeMarker": {
            "period": 14,  # 기간
        },
        "Donchian": {
            "period": 20,  # 기간
        },
        "Pivot": {
            "method": "standard",  # 피벗 포인트 계산 방법
        },
        "PSY": {
            "period": 12,  # 기간
        },
        "NPSY": {
            "period": 12,  # 기간
        },
    },
}

# 매매 시그널 설정
SIGNAL_THRESHOLDS = {
    "RSI": {
        "overbought": 70,  # 과매수 임계값
        "oversold": 30,  # 과매도 임계값
    },
    "CCI": {
        "overbought": 100,  # 과매수 임계값
        "oversold": -100,  # 과매도 임계값
    },
    "Stoch": {
        "overbought": 80,  # 과매수 임계값
        "oversold": 20,  # 과매도 임계값
    },
    "Williams": {
        "overbought": -20,  # 과매수 임계값
        "oversold": -80,  # 과매도 임계값
    },
    "CMO": {
        "overbought": 50,  # 과매수 임계값
        "oversold": -50,  # 과매도 임계값
    },
    "DeMarker": {
        "overbought": 0.8,  # 과매수 임계값
        "oversold": 0.2,  # 과매도 임계값
    },
    "PSY": {
        "overbought": 70,  # 과매수 임계값
        "oversold": 30,  # 과매도 임계값
    },
    "NPSY": {
        "overbought": 70,  # 과매수 임계값
        "oversold": 30,  # 과매도 임계값
    },
}

# 시그널 가중치 설정
SIGNAL_WEIGHTS = {
    "RSI": 0.2,
    "MACD": 0.2,
    "BB": 0.15,
    "Stoch": 0.15,
    "CCI": 0.1,
    "Williams": 0.1,
    "CMO": 0.1,
}

# 시각화 설정
VISUALIZATION_SETTINGS = {
    "figure_size": (15, 10),
    "style": "seaborn",
    "color_scheme": {
        "buy": "green",
        "sell": "red",
        "neutral": "gray",
    },
    "heatmap_cmap": "RdYlGn",
    "candlestick_colors": {
        "up": "#4dff4d",
        "down": "#ff4d4d",
    },
    "volume_colors": {
        "up": "lightcoral",
        "down": "lightblue",
    },
}
