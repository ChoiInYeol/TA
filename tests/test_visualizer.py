"""
시각화 모듈 테스트
"""

import os
import pandas as pd
import pytest
from src.visualizer import TradingVisualizer
from src.config import HEATMAP_FILE, SIGNALS_FILE, SPY_DATA_FILE

def test_visualizer_initialization():
    """TradingVisualizer 초기화 테스트"""
    visualizer = TradingVisualizer()
    assert visualizer is not None
    assert isinstance(visualizer, TradingVisualizer)

def test_visualizer_create_dashboard(tmp_path, sample_ohlcv_data, sample_signals_data):
    """대시보드 생성 테스트"""
    # 테스트용 파일 생성
    price_file = tmp_path / "test_price.csv"
    signals_file = tmp_path / "test_signals.csv"
    output_file = tmp_path / "test_heatmap.png"
    
    sample_ohlcv_data.to_csv(price_file)
    sample_signals_data.to_csv(signals_file)
    
    # 대시보드 생성
    visualizer = TradingVisualizer(
        signals_file=signals_file,
        price_file=price_file,
        output_file=output_file
    )
    visualizer.create_dashboard()
    
    # 결과 검증
    assert visualizer.fig is not None
    assert visualizer.merged_df is not None
    assert not visualizer.merged_df.empty

def test_visualizer_invalid_input():
    """잘못된 입력 테스트"""
    visualizer = TradingVisualizer()
    with pytest.raises(Exception):
        visualizer.create_dashboard()

def test_visualizer_save_dashboard(tmp_path, sample_ohlcv_data, sample_signals_data):
    """대시보드 저장 테스트"""
    # 테스트용 파일 생성
    price_file = tmp_path / "test_price.csv"
    signals_file = tmp_path / "test_signals.csv"
    output_file = tmp_path / "test_heatmap.png"
    
    sample_ohlcv_data.to_csv(price_file)
    sample_signals_data.to_csv(signals_file)
    
    # 대시보드 생성 및 저장
    visualizer = TradingVisualizer(
        signals_file=signals_file,
        price_file=price_file,
        output_file=output_file
    )
    visualizer.create_dashboard()
    visualizer.save_dashboard()
    
    # 저장된 파일 검증
    assert output_file.exists()

def test_visualizer_load_data(tmp_path, sample_ohlcv_data, sample_signals_data):
    """데이터 로드 테스트"""
    # 테스트용 파일 생성
    price_file = tmp_path / "test_price.csv"
    signals_file = tmp_path / "test_signals.csv"
    
    sample_ohlcv_data.to_csv(price_file)
    sample_signals_data.to_csv(signals_file)
    
    # 데이터 로드 테스트
    visualizer = TradingVisualizer()
    price_data, signals_data = visualizer._load_data(price_file, signals_file)
    
    pd.testing.assert_frame_equal(sample_ohlcv_data, price_data)
    pd.testing.assert_frame_equal(sample_signals_data, signals_data) 