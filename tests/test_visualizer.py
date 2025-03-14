"""
시각화 모듈 테스트
"""

import pytest

from visualizer import aligned_signal_candlestick


@pytest.fixture
def temp_output_file(tmp_path):
    """임시 출력 파일 경로 생성"""
    return tmp_path / "test_output.png"


def test_visualization_creation(
    sample_signals_data, sample_ohlcv_data, temp_output_file
):
    """시각화 생성 테스트"""
    # 임시 파일로 데이터 저장
    signals_file = temp_output_file.parent / "signals.csv"
    price_file = temp_output_file.parent / "prices.csv"

    sample_signals_data.to_csv(signals_file)
    sample_ohlcv_data.to_csv(price_file)

    # 시각화 생성
    aligned_signal_candlestick(
        signal_file=str(signals_file),
        price_file=str(price_file),
        last_n_trading_days=5,
        savefig=str(temp_output_file),
    )

    # 결과 확인
    assert temp_output_file.exists()
    assert temp_output_file.stat().st_size > 0


def test_visualization_with_invalid_files():
    """잘못된 파일 입력 테스트"""
    with pytest.raises(FileNotFoundError):
        aligned_signal_candlestick(
            signal_file="nonexistent_signals.csv",
            price_file="nonexistent_prices.csv",
            last_n_trading_days=5,
            savefig="test_output.png",
        )


def test_visualization_with_invalid_days():
    """잘못된 거래일 수 테스트"""
    with pytest.raises(ValueError):
        aligned_signal_candlestick(
            signal_file="test_signals.csv",
            price_file="test_prices.csv",
            last_n_trading_days=-1,
            savefig="test_output.png",
        )
