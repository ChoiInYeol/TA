"""
기술적 지표 모듈 테스트
"""

import pandas as pd
import numpy as np
import pytest
from src.technical_indicator import TechnicalIndicator
from src.config import TECHNICAL_INDICATORS

def test_technical_indicator_initialization():
    """TechnicalIndicator 초기화 테스트"""
    indicator = TechnicalIndicator()
    assert indicator is not None
    assert isinstance(indicator, TechnicalIndicator)

def test_technical_indicator_calculate_all(sample_ohlcv_data, tmp_path):
    """기술적 지표 계산 테스트"""
    # 테스트용 파일 생성
    data_file = tmp_path / "test_data.csv"
    output_file = tmp_path / "test_indicators.csv"
    sample_ohlcv_data.to_csv(data_file)
    
    # 지표 계산
    indicator = TechnicalIndicator(data_file=data_file, output_file=output_file)
    indicator.calculate_all()
    
    # 결과 검증
    assert indicator.indicators_df is not None
    assert not indicator.indicators_df.empty
    
    # 모멘텀 지표 검증
    for period in TECHNICAL_INDICATORS["모멘텀 지표"]["SMA"]["periods"]:
        assert f"SMA_{period}" in indicator.indicators_df.columns
    
    # 반대매매 지표 검증
    period = TECHNICAL_INDICATORS["반대매매 지표"]["RSI"]["period"]
    assert f"RSI({period})" in indicator.indicators_df.columns

def test_technical_indicator_invalid_input():
    """잘못된 입력 테스트"""
    indicator = TechnicalIndicator()
    with pytest.raises(Exception):
        indicator.calculate_all()

def test_technical_indicator_save_indicators(tmp_path, sample_ohlcv_data):
    """지표 저장 테스트"""
    # 테스트용 파일 생성
    data_file = tmp_path / "test_data.csv"
    output_file = tmp_path / "test_indicators.csv"
    sample_ohlcv_data.to_csv(data_file)
    
    # 지표 계산 및 저장
    indicator = TechnicalIndicator(data_file=data_file, output_file=output_file)
    indicator.calculate_all()
    indicator.save_indicators()
    
    # 저장된 파일 검증
    assert output_file.exists()
    saved_indicators = pd.read_csv(output_file)
    assert not saved_indicators.empty 