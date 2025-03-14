"""
시그널 생성 모듈 테스트
"""

import pandas as pd
import pytest

from signal_generator import SignalGenerator


def test_signal_generator_initialization(sample_indicators_data):
    """시그널 생성기 초기화 테스트"""
    generator = SignalGenerator(sample_indicators_data)
    assert generator.data is not None
    assert not generator.data.empty
    assert all(col in generator.data.columns for col in ["SMA_20", "RSI_14"])


def test_momentum_signal_generation(sample_indicators_data):
    """모멘텀 시그널 생성 테스트"""
    generator = SignalGenerator(sample_indicators_data)
    signals = generator.generate_momentum_signals()

    assert not signals.empty
    assert all(signals[col].isin([-1, 0, 1]).all() for col in signals.columns)
    assert all(not signals[col].isna().any() for col in signals.columns)


def test_contrarian_signal_generation(sample_indicators_data):
    """반추세 시그널 생성 테스트"""
    generator = SignalGenerator(sample_indicators_data)
    signals = generator.generate_contrarian_signals()

    assert not signals.empty
    assert all(signals[col].isin([-1, 0, 1]).all() for col in signals.columns)
    assert all(not signals[col].isna().any() for col in signals.columns)


def test_signal_values_range(sample_indicators_data):
    """시그널 값 범위 테스트"""
    generator = SignalGenerator(sample_indicators_data)

    momentum_signals = generator.generate_momentum_signals()
    contrarian_signals = generator.generate_contrarian_signals()

    for signals in [momentum_signals, contrarian_signals]:
        assert signals.min().min() >= -1
        assert signals.max().max() <= 1


def test_invalid_data_input():
    """잘못된 데이터 입력 테스트"""
    with pytest.raises(ValueError):
        SignalGenerator(None)

    with pytest.raises(ValueError):
        SignalGenerator(pd.DataFrame())
