"""
pytest 공통 fixture 정의
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_ohlcv_data():
    """샘플 OHLCV 데이터 생성

    Returns:
        pd.DataFrame: 테스트용 OHLCV 데이터
    """
    dates = pd.date_range(start="2023-01-01", end="2023-01-10", freq="D")
    data = {
        "Open": [100, 102, 101, 103, 102, 104, 103, 105, 104, 106],
        "High": [103, 104, 103, 105, 104, 106, 105, 107, 106, 108],
        "Low": [99, 100, 99, 101, 100, 102, 101, 103, 102, 104],
        "Close": [102, 101, 103, 102, 104, 103, 105, 104, 106, 105],
        "Volume": [1000, 1100, 900, 1200, 1000, 1300, 1100, 1400, 1200, 1500],
    }
    return pd.DataFrame(data, index=dates)


@pytest.fixture
def sample_indicators_data(sample_ohlcv_data):
    """샘플 기술적 지표 데이터 생성

    Args:
        sample_ohlcv_data (pd.DataFrame): 기본 OHLCV 데이터

    Returns:
        pd.DataFrame: 테스트용 기술적 지표 데이터
    """
    data = sample_ohlcv_data.copy()
    # 샘플 기술적 지표 추가
    data["SMA_20"] = 102.5
    data["RSI_14"] = 55.0
    return data


@pytest.fixture
def sample_signals_data(sample_ohlcv_data):
    """샘플 트레이딩 시그널 데이터 생성

    Args:
        sample_ohlcv_data (pd.DataFrame): 기본 OHLCV 데이터

    Returns:
        pd.DataFrame: 테스트용 트레이딩 시그널 데이터
    """
    dates = sample_ohlcv_data.index
    data = {
        "SMA_Signal": [1, 0, -1, 1, 0, -1, 1, 0, -1, 1],
        "RSI_Signal": [-1, 1, 0, -1, 1, 0, -1, 1, 0, -1],
    }
    return pd.DataFrame(data, index=dates)
