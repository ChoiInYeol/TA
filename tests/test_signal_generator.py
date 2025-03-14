"""
시그널 생성 모듈 테스트
"""

import pandas as pd
import pytest
from src.signal_generator import SignalGenerator
from src.config import TECHNICAL_INDICATORS, SIGNAL_THRESHOLDS

def test_signal_generator_initialization():
    """SignalGenerator 초기화 테스트"""
    generator = SignalGenerator()
    assert generator is not None
    assert isinstance(generator, SignalGenerator)

def test_signal_generator_generate_all(tmp_path, sample_indicators_data):
    """시그널 생성 테스트"""
    # 테스트용 파일 생성
    indicators_file = tmp_path / "test_indicators.csv"
    output_file = tmp_path / "test_signals.csv"
    sample_indicators_data.to_csv(indicators_file)
    
    # 시그널 생성
    generator = SignalGenerator(indicators_file=indicators_file, output_file=output_file)
    generator.generate_all()
    
    # 결과 검증
    assert generator.signals_df is not None
    assert not generator.signals_df.empty
    
    # 모멘텀 지표 시그널 검증
    for period in TECHNICAL_INDICATORS["모멘텀 지표"]["SMA"]["periods"]:
        assert f"SMA_{period}_Signal" in generator.signals_df.columns
    
    # 반대매매 지표 시그널 검증
    period = TECHNICAL_INDICATORS["반대매매 지표"]["RSI"]["period"]
    assert f"RSI({period})_Signal" in generator.signals_df.columns

def test_signal_generator_invalid_input():
    """잘못된 입력 테스트"""
    generator = SignalGenerator()
    with pytest.raises(Exception):
        generator.generate_all()

def test_signal_generator_save_signals(tmp_path, sample_indicators_data):
    """시그널 저장 테스트"""
    # 테스트용 파일 생성
    indicators_file = tmp_path / "test_indicators.csv"
    output_file = tmp_path / "test_signals.csv"
    sample_indicators_data.to_csv(indicators_file)
    
    # 시그널 생성 및 저장
    generator = SignalGenerator(indicators_file=indicators_file, output_file=output_file)
    generator.generate_all()
    generator.save_signals()
    
    # 저장된 파일 검증
    assert output_file.exists()
    saved_signals = pd.read_csv(output_file)
    assert not saved_signals.empty 