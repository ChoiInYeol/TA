"""
기술적 지표 계산 모듈 테스트
"""
import numpy as np
import pytest

from technical_indicator import CORE16MomentumIndicator, CORE16ContrarianIndicator

def test_momentum_indicator_initialization(sample_ohlcv_data):
    """모멘텀 지표 초기화 테스트"""
    indicator = CORE16MomentumIndicator(sample_ohlcv_data)
    assert indicator.data is not None
    assert not indicator.data.empty
    assert all(col in indicator.data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])

def test_contrarian_indicator_initialization(sample_ohlcv_data):
    """반추세 지표 초기화 테스트"""
    indicator = CORE16ContrarianIndicator(sample_ohlcv_data)
    assert indicator.data is not None
    assert not indicator.data.empty
    assert all(col in indicator.data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])

def test_momentum_indicator_calculation(sample_ohlcv_data):
    """모멘텀 지표 계산 테스트"""
    indicator = CORE16MomentumIndicator(sample_ohlcv_data)
    result = indicator.calculate_all_indicators()
    
    assert not result.empty
    assert all(not result[col].isna().all() for col in result.columns)
    assert all(result[col].dtype == np.float64 for col in result.columns)

def test_contrarian_indicator_calculation(sample_ohlcv_data):
    """반추세 지표 계산 테스트"""
    indicator = CORE16ContrarianIndicator(sample_ohlcv_data)
    result = indicator.calculate_all_indicators()
    
    assert not result.empty
    assert all(not result[col].isna().all() for col in result.columns)
    assert all(result[col].dtype == np.float64 for col in result.columns)

def test_invalid_data_input():
    """잘못된 데이터 입력 테스트"""
    with pytest.raises(ValueError):
        CORE16MomentumIndicator(None)
    
    with pytest.raises(ValueError):
        CORE16ContrarianIndicator(None) 