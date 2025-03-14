"""
테스트 설정 및 fixture 모듈
"""

import os
import sys
import pandas as pd
import pytest
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def sample_ohlcv_data():
    """샘플 OHLCV 데이터 생성"""
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    data = {
        "Date": dates,
        "Open": [100.0] * 100,
        "High": [105.0] * 100,
        "Low": [95.0] * 100,
        "Close": [102.0] * 100,
        "Volume": [1000000] * 100
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_indicators_data(sample_ohlcv_data):
    """샘플 기술적 지표 데이터 생성"""
    df = sample_ohlcv_data.copy()
    
    # 모멘텀 지표 추가
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["MACD"] = df["Close"].ewm(span=12, adjust=False).mean() - df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    
    # 반대매매 지표 추가
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI_14"] = 100 - (100 / (1 + rs))
    
    return df

@pytest.fixture
def sample_signals_data(sample_indicators_data):
    """샘플 매매 시그널 데이터 생성"""
    df = pd.DataFrame({"Date": sample_indicators_data["Date"]})
    
    # 모멘텀 지표 시그널
    df["SMA_20_Signal"] = (sample_indicators_data["Close"] > sample_indicators_data["SMA_20"]).astype(int)
    df["MACD_Signal"] = (sample_indicators_data["MACD"] > sample_indicators_data["MACD_Signal"]).astype(int)
    
    # 반대매매 지표 시그널
    df["RSI_14_Signal"] = 0
    df.loc[sample_indicators_data["RSI_14"] < 30, "RSI_14_Signal"] = 1
    df.loc[sample_indicators_data["RSI_14"] > 70, "RSI_14_Signal"] = -1
    
    return df 